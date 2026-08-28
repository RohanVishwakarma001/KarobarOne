# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/approvalService.py — Approval Workflow Engine (Core Service)
# ================================================================================
# Why this file is used:
#   - Central service encapsulating ALL approval workflow business logic.
#   - Handles draft creation, submission, approval, rejection, publishing,
#     rollback, and audit trail generation for the Change Request system.
#
# What components are inside:
#   - MODEL_MAP         -> Maps entityType strings to SQLAlchemy model classes
#                          for dynamic publishing of approved changes.
#   - ApprovalService   -> Main service class with methods:
#       - createDraft()          -> Save pending entity changes as draft version
#       - submitForApproval()    -> Submit change request + seed review queue
#       - updatePendingDraft()   -> Modify versionData of PENDING request
#       - withdrawRequest()      -> Cancel PENDING request + cleanup
#       - approveRequest()       -> Approve + trigger publish + audit
#       - rejectRequest()        -> Reject + store remarks + audit
#       - rollbackEntity()       -> Restore entity to historical version
#       - _publishToLiveTable()  -> (private) Apply approved data to live DB row
#       - _snapshotCurrentState()-> (private) Capture current entity state before changes
#       - _createAuditLog()      -> (private) Log workflow actions to AuditLog table
# ================================================================================
"""
Approval Workflow Engine.

Provides the full lifecycle management for change requests:
draft → submit → review queue → approve/reject → publish → version history.

All methods use flush() (via repositories) for transactional safety.
The session dependency (getDb) handles commit/rollback at the request boundary.
"""

# Import datetime for timestamping review and audit events
from datetime import datetime
# Import Any for flexible type annotations in method signatures
from typing import Any, Dict, Optional
# Import uuid for generating unique identifiers in new records
import uuid

# Import SQLAlchemy inspection utility to dynamically map model column names
from sqlalchemy import inspect as sa_inspect
# Import select for building ad-hoc queries not covered by repositories
from sqlalchemy import select
# Import async session type for database transaction management
from sqlalchemy.ext.asyncio import AsyncSession

# Import database model classes for approval workflow entities
from app.db.models.approvals import (
    ApprovalRequest,        # Stores approval request metadata and status
    ApprovalRequestVersion, # Tracks review history snapshots per request
    EntityVersion,          # Stores JSON snapshots of entity data
    AuditLog,               # Records all workflow actions for audit trail
    ReviewQueue,            # Manages review assignment queue
)

# Import repository classes for structured data access
from app.repositories.approvalRequestRepository import ApprovalRequestRepository  # Approval request queries
from app.repositories.entityVersionRepository import EntityVersionRepository       # Entity version queries
from app.repositories.reviewQueueRepository import ReviewQueueRepository           # Review queue queries

# Import custom exception for business rule violations
from app.core.exceptionsCompat import (
    NotFoundError,             # Raised when a requested resource does not exist
    ConflictError,             # Raised when a duplicate or conflicting resource is found
    BusinessValidationError,   # Raised when a business workflow rule is violated
)

# Import entity model classes for the publishing engine (MODEL_MAP)
from app.db.models.store import Store             # Store entity model
from app.db.models.section import Section         # Section entity model
from app.db.models.brands import Brand            # Brand entity model
from app.db.models.categories import Category     # Category entity model
from app.db.models.website import Website         # Website entity model
from app.productsPorted.models.models import Product  # Product entity model

# ─────────────────────────────────────────────
# MODEL_MAP: Maps entityType strings to SQLAlchemy model classes.
# Used by the publishing engine to dynamically resolve which
# database table to update when an approved change is published.
# ─────────────────────────────────────────────
MODEL_MAP: Dict[str, Any] = {
    "STORE": Store,
    "SECTION": Section,
    "BRAND": Brand,
    "CATEGORY": Category,
    "PRODUCT": Product,
    "WEBSITE": Website,
    "website": Website,
    "product": Product,
    "brand": Brand,
    "category": Category,
    "store": Store,
    "section": Section,
}


class ApprovalService:
    """
    Central service class encapsulating all approval workflow business logic.

    This service orchestrates the full lifecycle of change requests:
    1. Draft creation (saving pending changes without submitting)
    2. Submission for approval (creates review queue entry)
    3. Draft modification (only while PENDING)
    4. Request withdrawal (only while PENDING)
    5. Approval (triggers publishing engine + audit logging)
    6. Rejection (stores remarks + audit logging)
    7. Entity rollback (restores to a previous version)

    All database mutations use repository flush() pattern.
    The calling endpoint's session dependency handles commit/rollback.
    """

    def __init__(self, session: AsyncSession):
        """
        What it does:
            Initializes the service and binds standard repository instances to the active session.
        Why it is used:
            Provides the database execution context for all workflow methods.
        """
        self.session = session
        # Initialize repository instances for each approval-related entity
        self.approvalRepo = ApprovalRequestRepository(ApprovalRequest, session)
        self.versionRepo = EntityVersionRepository(EntityVersion, session)
        self.queueRepo = ReviewQueueRepository(ReviewQueue, session)

    # ═══════════════════════════════════════════════
    # STORY 1: CHANGE REQUESTS
    # ═══════════════════════════════════════════════

    async def createDraft(
        self,
        tenantId: uuid.UUID,
        entityType: str,
        entityId: uuid.UUID,
        versionData: Dict[str, Any],
        createdBy: uuid.UUID,
    ) -> EntityVersion:
        """
        What it does:
            Saves entity changes as an unpublished draft snapshot (isPublished=False).
            Automatically queries and increments the next version sequence number.
            Generates a CREATE action entry in the system audit trail.
        Why it is used:
            Allows merchant stores to save their pending updates in the database
            without submitting them immediately to platform staff for review.
        """
        # Get the next version number for this entity
        latestVersion = await self.versionRepo.getLatestVersionNumber(entityType, entityId)
        nextVersion = latestVersion + 1

        # Create the draft entity version
        draft = EntityVersion(
            tenantId=tenantId,
            entityType=entityType,
            entityId=entityId,
            versionNumber=nextVersion,
            versionData=versionData,
            isPublished=False,
            createdBy=createdBy,
        )
        draft = await self.versionRepo.create(draft)

        # Log the draft creation in audit trail
        await self._createAuditLog(
            tenantId=tenantId,
            entityType=entityType,
            entityId=entityId,
            actionType="CREATE",
            newValue=versionData,
            performedBy=createdBy,
        )

        return draft

    async def submitForApproval(
        self,
        tenantId: uuid.UUID,
        entityType: str,
        entityId: uuid.UUID,
        operationType: str,
        versionData: Dict[str, Any],
        submittedBy: uuid.UUID,
        remarks: Optional[str] = None,
    ) -> ApprovalRequest:
        """
        What it does:
            Creates an EntityVersion snapshot and a corresponding PENDING ApprovalRequest.
            Validates that no concurrent PENDING request exists for the same entity.
            Seeds an active task entry in the ReviewQueue for reviewer assignment.
            Logs the submission action in the audit trail.
        Why it is used:
            Implements the submission workflow for change requests. Enforces integrity checks
            (no duplicate active reviews) and notifies platform managers by queueing the request.
        """
        # Check for duplicate pending request for the same entity
        existing = await self.approvalRepo.getPendingByEntity(tenantId, entityType, entityId)
        if existing:
            raise ConflictError(
                f"A PENDING approval request already exists for {entityType} with ID {entityId}"
            )

        # Create entity version snapshot
        latestVersion = await self.versionRepo.getLatestVersionNumber(entityType, entityId)
        nextVersion = latestVersion + 1

        entityVersion = EntityVersion(
            tenantId=tenantId,
            entityType=entityType,
            entityId=entityId,
            versionNumber=nextVersion,
            versionData=versionData,
            isPublished=False,
            createdBy=submittedBy,
        )
        entityVersion = await self.versionRepo.create(entityVersion)

        # Create approval request
        approvalRequest = ApprovalRequest(
            tenantId=tenantId,
            entityType=entityType,
            entityId=entityId,
            operationType=operationType,
            submittedVersionNumber=nextVersion,
            approvalStatus="PENDING",
            submittedBy=submittedBy,
            remarks=remarks,
        )
        approvalRequest = await self.approvalRepo.create(approvalRequest)

        # Seed review queue entry for this request
        queueEntry = ReviewQueue(
            approvalRequestId=approvalRequest.id,
            priority="MEDIUM",
        )
        await self.queueRepo.create(queueEntry)

        # Log the submission event
        await self._createAuditLog(
            tenantId=tenantId,
            entityType=entityType,
            entityId=entityId,
            actionType="CREATE",
            newValue={"approvalRequestId": str(approvalRequest.id), "operationType": operationType},
            performedBy=submittedBy,
        )

        return approvalRequest

    async def updatePendingDraft(
        self,
        requestId: uuid.UUID,
        versionData: Dict[str, Any],
    ) -> EntityVersion:
        """
        What it does:
            Modifies the versionData payload inside the EntityVersion linked to a PENDING request.
            Checks that the request exists and is in 'PENDING' status before modifying.
        Why it is used:
            Implements the "Update Request API" workflow. Enforces state validation rules
            that forbid editing drafts once they are approved or rejected.
        """
        # Fetch and validate the approval request
        request = await self.approvalRepo.getById(requestId)
        if not request:
            raise NotFoundError("ApprovalRequest", str(requestId))

        # Enforce workflow rule: only PENDING requests can be edited
        if request.approvalStatus != "PENDING":
            raise BusinessValidationError(
                f"Cannot edit request with status '{request.approvalStatus}'. Only PENDING requests are editable."
            )

        # Find the entity version associated with this request
        result = await self.session.execute(
            select(EntityVersion).where(
                EntityVersion.entityType == request.entityType,
                EntityVersion.entityId == request.entityId,
                EntityVersion.versionNumber == request.submittedVersionNumber,
            )
        )
        entityVersion = result.scalar_one_or_none()
        if not entityVersion:
            raise NotFoundError("EntityVersion", f"version {request.submittedVersionNumber}")

        # Update the version data
        entityVersion = await self.versionRepo.update(entityVersion, {"versionData": versionData})
        return entityVersion

    async def withdrawRequest(self, requestId: uuid.UUID) -> None:
        """
        What it does:
            Cancels a pending request by removing the ApprovalRequest and ReviewQueue rows.
            Checks that the request exists and is in PENDING status before deleting.
            Logs a DELETE action in the audit trail.
        Why it is used:
            Implements the "Withdraw Request API" workflow. Enforces state validation rules
            that forbid cancelling requests that are already processed.
        """
        # Fetch and validate the approval request
        request = await self.approvalRepo.getById(requestId)
        if not request:
            raise NotFoundError("ApprovalRequest", str(requestId))

        # Enforce workflow rule: only PENDING requests can be withdrawn
        if request.approvalStatus != "PENDING":
            raise BusinessValidationError(
                f"Cannot withdraw request with status '{request.approvalStatus}'. Only PENDING requests can be withdrawn."
            )

        # Remove the review queue entry (if exists)
        queueEntry = await self.queueRepo.getByApprovalRequestId(requestId)
        if queueEntry:
            await self.queueRepo.delete(queueEntry)

        # Log withdrawal before deleting the request
        await self._createAuditLog(
            tenantId=request.tenantId,
            entityType=request.entityType,
            entityId=request.entityId,
            actionType="DELETE",
            oldValue={"approvalRequestId": str(requestId), "status": "PENDING"},
            performedBy=request.submittedBy,
        )

        # Delete the approval request (cascades to versions via relationship)
        await self.approvalRepo.delete(request)

    # ═══════════════════════════════════════════════
    # STORY 3: APPROVAL
    # ═══════════════════════════════════════════════

    async def approveRequest(
        self,
        requestId: uuid.UUID,
        reviewedBy: uuid.UUID,
        remarks: Optional[str] = None,
    ) -> ApprovalRequest:
        """
        What it does:
            Sets ApprovalRequest to APPROVED, generates an ApprovalRequestVersion review log,
            snapshots current live state, publishes changes to live table, marks EntityVersion as published,
            and cleans up the review queue task. Generates an APPROVE audit log.
        Why it is used:
            Core entry point for approving changes. Validates status constraints, triggers
            data propagation, maintains rollback snapshots, and completes queue entries.
        """
        # Fetch and validate the approval request
        request = await self.approvalRepo.getById(requestId)
        if not request:
            raise NotFoundError("ApprovalRequest", str(requestId))

        if request.approvalStatus != "PENDING":
            raise BusinessValidationError(
                f"Cannot approve request with status '{request.approvalStatus}'. Only PENDING requests can be approved."
            )

        # Update approval status
        now = datetime.now()
        request = await self.approvalRepo.update(request, {
            "approvalStatus": "APPROVED",
            "reviewedBy": reviewedBy,
            "reviewedAt": now,
            "remarks": remarks,
        })

        # Create review history version
        reviewVersion = ApprovalRequestVersion(
            approvalRequestId=requestId,
            versionNumber=request.submittedVersionNumber,
            approvalStatus="APPROVED",
            reviewedBy=reviewedBy,
            reviewComment=remarks,
            reviewedAt=now,
        )
        self.session.add(reviewVersion)
        await self.session.flush()

        # Fetch the entity version to publish
        result = await self.session.execute(
            select(EntityVersion).where(
                EntityVersion.entityType == request.entityType,
                EntityVersion.entityId == request.entityId,
                EntityVersion.versionNumber == request.submittedVersionNumber,
            )
        )
        entityVersion = result.scalar_one_or_none()

        if entityVersion:
            # Snapshot current live state before publishing (for rollback capability)
            await self._snapshotCurrentState(
                tenantId=request.tenantId,
                entityType=request.entityType,
                entityId=request.entityId,
                performedBy=reviewedBy,
            )

            # Publish approved changes to the live table
            await self._publishToLiveTable(
                entityType=request.entityType,
                entityId=request.entityId,
                operationType=request.operationType,
                versionData=entityVersion.versionData,
            )

            # Mark this version as published, unpublish all previous versions
            await self.versionRepo.unpublishAllForEntity(request.entityType, request.entityId)
            await self.versionRepo.update(entityVersion, {"isPublished": True})

        # Remove from review queue
        queueEntry = await self.queueRepo.getByApprovalRequestId(requestId)
        if queueEntry:
            await self.queueRepo.delete(queueEntry)

        # Log approval event
        await self._createAuditLog(
            tenantId=request.tenantId,
            entityType=request.entityType,
            entityId=request.entityId,
            actionType="APPROVE",
            newValue={"approvalRequestId": str(requestId), "reviewedBy": str(reviewedBy)},
            performedBy=reviewedBy,
        )

        # Notify store owner/requester (TC-0088, TC-0097)
        if hasattr(request, "submittedBy") and request.submittedBy:
            from app.services.notificationService import NotificationService
            await NotificationService.notify_approval_result(
                store_owner_id=request.submittedBy,
                entity_type=request.entityType,
                entity_name=getattr(request, "title", None) or str(request.entityId),
                approved=True,
                reviewer_notes=remarks,
            )

        return request

    # ═══════════════════════════════════════════════
    # STORY 4: REJECTION
    # ═══════════════════════════════════════════════

    async def rejectRequest(
        self,
        requestId: uuid.UUID,
        reviewedBy: uuid.UUID,
        rejectionReason: str,
        remarks: Optional[str] = None,
    ) -> ApprovalRequest:
        """
        What it does:
            Sets ApprovalRequest status to REJECTED with comments, creates a review history version,
            removes the queue task, and generates audit logs for the rejection and notification.
        Why it is used:
            Implements the rejection workflow. Ensures a mandatory rejection reason is stored,
            releases queue tasks, and triggers notification alerts.
        """
        # Fetch and validate the approval request
        request = await self.approvalRepo.getById(requestId)
        if not request:
            raise NotFoundError("ApprovalRequest", str(requestId))

        if request.approvalStatus != "PENDING":
            raise BusinessValidationError(
                f"Cannot reject request with status '{request.approvalStatus}'. Only PENDING requests can be rejected."
            )

        # Update rejection status
        now = datetime.now()
        request = await self.approvalRepo.update(request, {
            "approvalStatus": "REJECTED",
            "reviewedBy": reviewedBy,
            "reviewedAt": now,
            "rejectionReason": rejectionReason,
            "remarks": remarks,
        })

        # Create review history version
        reviewVersion = ApprovalRequestVersion(
            approvalRequestId=requestId,
            versionNumber=request.submittedVersionNumber,
            approvalStatus="REJECTED",
            reviewedBy=reviewedBy,
            reviewComment=rejectionReason,
            reviewedAt=now,
        )
        self.session.add(reviewVersion)
        await self.session.flush()

        # Remove from review queue
        queueEntry = await self.queueRepo.getByApprovalRequestId(requestId)
        if queueEntry:
            await self.queueRepo.delete(queueEntry)

        # Log rejection event
        await self._createAuditLog(
            tenantId=request.tenantId,
            entityType=request.entityType,
            entityId=request.entityId,
            actionType="REJECT",
            newValue={
                "approvalRequestId": str(requestId),
                "reviewedBy": str(reviewedBy),
                "rejectionReason": rejectionReason,
            },
            performedBy=reviewedBy,
        )

        # Log notification event (extensible hook for future email/SMS/webhook integration)
        await self._createAuditLog(
            tenantId=request.tenantId,
            entityType="APPROVAL_REQUEST",
            entityId=requestId,
            actionType="REJECT",
            newValue={
                "notification": True,
                "targetUser": str(request.submittedBy),
                "message": f"Your {request.entityType} change request was rejected: {rejectionReason}",
            },
            performedBy=reviewedBy,
        )

        # Notify store owner/requester (TC-0089, TC-0097)
        if hasattr(request, "submittedBy") and request.submittedBy:
            from app.services.notificationService import NotificationService
            await NotificationService.notify_approval_result(
                store_owner_id=request.submittedBy,
                entity_type=request.entityType,
                entity_name=getattr(request, "title", None) or str(request.entityId),
                approved=False,
                reviewer_notes=rejectionReason,
            )

        return request

    # ═══════════════════════════════════════════════
    # STORY 6: VERSIONING & ROLLBACK
    # ═══════════════════════════════════════════════

    async def rollbackEntity(
        self,
        versionId: uuid.UUID,
        performedBy: uuid.UUID,
    ) -> EntityVersion:
        """
        What it does:
            Restores the live database entity state to match a historical EntityVersion snapshot.
            Snapshots the pre-rollback state, applies historical version data, unpublishes older versions,
            creates a new published version entry, and records a RESTORE audit log.
        Why it is used:
            Implements the "Rollback API" workflow, allowing merchants or platform managers
            to safely undo incorrect changes and restore working configurations.
        """
        # Fetch the historical version to restore
        historicalVersion = await self.versionRepo.getById(versionId)
        if not historicalVersion:
            raise NotFoundError("EntityVersion", str(versionId))

        # Snapshot current live state before rollback
        oldState = await self._snapshotCurrentState(
            tenantId=historicalVersion.tenantId,
            entityType=historicalVersion.entityType,
            entityId=historicalVersion.entityId,
            performedBy=performedBy,
        )

        # Apply historical data to the live table
        await self._publishToLiveTable(
            entityType=historicalVersion.entityType,
            entityId=historicalVersion.entityId,
            operationType="UPDATE",
            versionData=historicalVersion.versionData,
        )

        # Create a new version marked as published (the rollback result)
        latestVersion = await self.versionRepo.getLatestVersionNumber(
            historicalVersion.entityType, historicalVersion.entityId
        )
        newVersion = EntityVersion(
            tenantId=historicalVersion.tenantId,
            entityType=historicalVersion.entityType,
            entityId=historicalVersion.entityId,
            versionNumber=latestVersion + 1,
            versionData=historicalVersion.versionData,
            isPublished=True,
            createdBy=performedBy,
        )

        # Unpublish all existing versions and mark the new one as published
        await self.versionRepo.unpublishAllForEntity(
            historicalVersion.entityType, historicalVersion.entityId
        )
        newVersion = await self.versionRepo.create(newVersion)

        # Log the RESTORE event
        await self._createAuditLog(
            tenantId=historicalVersion.tenantId,
            entityType=historicalVersion.entityType,
            entityId=historicalVersion.entityId,
            actionType="RESTORE",
            oldValue=oldState,
            newValue=historicalVersion.versionData,
            performedBy=performedBy,
        )

        return newVersion

    # ═══════════════════════════════════════════════
    # STORY 5: PUBLISHING ENGINE (Private Methods)
    # ═══════════════════════════════════════════════

    async def _publishToLiveTable(
        self,
        entityType: str,
        entityId: uuid.UUID,
        operationType: str,
        versionData: Dict[str, Any],
    ) -> None:
        """
        What it does:
            Maps entityType string to its corresponding live database model class.
            Uses SQLAlchemy inspection to filter out invalid fields from the snapshot,
            then performs a CREATE, UPDATE, or DELETE operation directly on the live row.
        Why it is used:
            Translates approved JSON snapshots (`versionData`) into actual modifications
            on the live application database tables (Publishing Engine).
        """
        # Resolve the target model class from MODEL_MAP
        modelClass = MODEL_MAP.get(entityType)
        if not modelClass:
            # Entity type not yet supported for publishing — log but don't fail
            # This allows approval workflow to work for entity types that aren't
            # in MODEL_MAP yet (the approval/version data is still saved)
            return

        if operationType == "CREATE":
            # Insert a new row with the version data
            validColumns = {c.key for c in sa_inspect(modelClass).mapper.column_attrs}
            filteredData = {k: v for k, v in versionData.items() if k in validColumns}
            filteredData["id"] = entityId  # Ensure the entity ID matches
            newEntity = modelClass(**filteredData)
            self.session.add(newEntity)
            await self.session.flush()

        elif operationType == "UPDATE":
            # Update existing row with version data columns
            existingEntity = await self.session.get(modelClass, entityId)
            if not existingEntity:
                raise NotFoundError(entityType, str(entityId))

            validColumns = {c.key for c in sa_inspect(modelClass).mapper.column_attrs}
            filteredData = {k: v for k, v in versionData.items() if k in validColumns}
            # Exclude primary key and auto-generated fields from update
            filteredData.pop("id", None)
            filteredData.pop("createdAt", None)

            for key, value in filteredData.items():
                setattr(existingEntity, key, value)
            await self.session.flush()

        elif operationType == "DELETE":
            # Hard-delete the existing row
            existingEntity = await self.session.get(modelClass, entityId)
            if not existingEntity:
                raise NotFoundError(entityType, str(entityId))
            await self.session.delete(existingEntity)
            await self.session.flush()

    async def _snapshotCurrentState(
        self,
        tenantId: uuid.UUID,
        entityType: str,
        entityId: uuid.UUID,
        performedBy: uuid.UUID,
    ) -> Optional[Dict[str, Any]]:
        """
        What it does:
            Queries the live database table for an entity, converts its columns
            and their values into a JSON-serializable dictionary.
        Why it is used:
            Generates pre-modification snapshots to store in the audit logs (`oldValue`)
            and to support future rollback versions.
        """
        modelClass = MODEL_MAP.get(entityType)
        if not modelClass:
            return None

        existingEntity = await self.session.get(modelClass, entityId)
        if not existingEntity:
            return None

        # Convert the live entity to a JSON-serializable dictionary
        validColumns = {c.key for c in sa_inspect(modelClass).mapper.column_attrs}
        currentState = {}
        for col in validColumns:
            value = getattr(existingEntity, col, None)
            if value is not None:
                # Convert UUID and datetime objects to strings for JSON storage
                if isinstance(value, uuid.UUID):
                    currentState[col] = str(value)
                elif isinstance(value, datetime):
                    currentState[col] = value.isoformat()
                else:
                    currentState[col] = value

        return currentState

    async def _createAuditLog(
        self,
        tenantId: uuid.UUID,
        entityType: str,
        entityId: uuid.UUID,
        actionType: str,
        performedBy: uuid.UUID,
        oldValue: Optional[Dict[str, Any]] = None,
        newValue: Optional[Dict[str, Any]] = None,
        changedFields: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """
        What it does:
            Creates and inserts a new AuditLog record inside the database context.
        Why it is used:
            Provides a central private method to log any workflow action (approvals,
            rejections, drafts, rollbacks) to ensure compliance and history tracking.
        """
        auditLog = AuditLog(
            tenantId=tenantId,
            entityType=entityType,
            entityId=entityId,
            actionType=actionType,
            oldValue=oldValue,
            newValue=newValue,
            changedFields=changedFields,
            performedBy=performedBy,
        )
        self.session.add(auditLog)
        await self.session.flush()
        return auditLog
