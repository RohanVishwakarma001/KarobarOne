# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: tests/test_change_request_approval.py — Approval Engine Unit Tests
# ================================================================================
# Why this file is used:
#   - Verifies the functional correctness of the approval engine, change requests,
#     review queue, publishing engine, and version rollback flows.
#   - Uses an in-memory SQLite database with PostgreSQL type translation overrides.
# ================================================================================
"""
Unit tests for the Change Request and Approval Engine workflow.
"""

# Import asyncio for async tests handling
import asyncio
# Import pytest for testing framework
import pytest
# Import pytest_asyncio for async fixtures
import pytest_asyncio
# Import uuid for entity lookup identifiers
import uuid

# Import SQLAlchemy async DB engine and session maker tools
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# Import select query builder from SQLAlchemy
from sqlalchemy import select
# Import compilation rules from SQLAlchemy extension
from sqlalchemy.ext.compiler import compiles
# Import Postgres-specific types for custom SQLite compilation overrides
from sqlalchemy.dialects.postgresql import JSONB, UUID as PostgresUUID, INET as PostgresINET

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    """Compiles PG-specific JSONB to standard SQLite JSON."""
    return "JSON"

@compiles(PostgresUUID, "sqlite")
def compile_uuid_sqlite(type_, compiler, **kw):
    """Compiles PG-specific UUID to SQLite VARCHAR."""
    return "VARCHAR(36)"

@compiles(PostgresINET, "sqlite")
def compile_inet_sqlite(type_, compiler, **kw):
    """Compiles PG-specific INET to SQLite VARCHAR."""
    return "VARCHAR(45)"

# Import declarative Base mapping
from app.db.base import Base
# Import central models registry to load ORM schemas
from app.db.modelsRegistry import *

# Import backend business logic services
from app.services.approvalService import ApprovalService
from app.core.exceptionsCompat import ConflictError, BusinessValidationError


@pytest_asyncio.fixture(scope="function")
async def testDb():
    """
    Creates an in-memory SQLite database, runs DDL tables creation for required models,
    yields a transaction-scoped AsyncSession, and tears down the database after test completion.
    """
    # Create in-memory SQLite engine for fast concurrent testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    # Specific tables list required for approval engine tests
    tables_to_create = [
        ApprovalRequest.__table__,
        ApprovalRequestVersion.__table__,
        EntityVersion.__table__,
        AuditLog.__table__,
        StatusHistory.__table__,
        ReviewQueue.__table__,
        Brand.__table__,
        BrandApproval.__table__,
    ]

    async with engine.begin() as conn:
        # Create specific tables to avoid SQLite compilation errors with unsupported operators (e.g. tags ~ regex)
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=tables_to_create))

    # Instantiate async session maker
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        yield session

    # Drop tables during teardown
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.drop_all(sync_conn, tables=tables_to_create))
    await engine.dispose()


@pytest.mark.asyncio
async def test_draft_creation_and_update(testDb):
    """
    Verifies that drafts are created successfully as unpublished EntityVersion models,
    and can be modified while the request is PENDING.
    """
    service = ApprovalService(testDb)
    tenant_id = uuid.uuid4()
    entity_id = uuid.uuid4()
    user_id = uuid.uuid4()

    # 1. Create a draft version
    draft_data = {"name": "Old Brand Name", "websiteUrl": "https://old.com"}
    draft = await service.createDraft(
        tenantId=tenant_id,
        entityType="BRAND",
        entityId=entity_id,
        versionData=draft_data,
        createdBy=user_id,
    )

    assert draft.id is not None
    assert draft.versionNumber == 1
    assert draft.isPublished is False
    assert draft.versionData == draft_data

    # 2. Check audit log for CREATE action
    audit_check = await testDb.execute(
        select(AuditLog).where(AuditLog.entityId == entity_id).where(AuditLog.actionType == "CREATE")
    )
    audit = audit_check.scalar_one_or_none()
    assert audit is not None
    assert audit.newValue == draft_data

    # 3. Create an approval request for this draft
    req = await service.submitForApproval(
        tenantId=tenant_id,
        entityType="BRAND",
        entityId=entity_id,
        operationType="CREATE",
        versionData=draft_data,
        submittedBy=user_id,
        remarks="Submitting initial brand details",
    )

    assert req.id is not None
    assert req.approvalStatus == "PENDING"
    assert req.submittedVersionNumber == 2  # The submit method increments version

    # 4. Modify the pending draft's version data
    updated_data = {"name": "New Brand Name", "websiteUrl": "https://new.com"}
    updated_version = await service.updatePendingDraft(
        requestId=req.id,
        versionData=updated_data,
    )

    assert updated_version.versionNumber == 2
    assert updated_version.versionData == updated_data


@pytest.mark.asyncio
async def test_duplicate_pending_request_prevention(testDb):
    """
    Ensures that multiple PENDING requests cannot be created for the same entity concurrently.
    """
    service = ApprovalService(testDb)
    tenant_id = uuid.uuid4()
    entity_id = uuid.uuid4()
    user_id = uuid.uuid4()

    draft_data = {"name": "Brand A"}

    # Submit first request successfully
    req1 = await service.submitForApproval(
        tenantId=tenant_id,
        entityType="BRAND",
        entityId=entity_id,
        operationType="CREATE",
        versionData=draft_data,
        submittedBy=user_id,
    )
    assert req1.approvalStatus == "PENDING"

    # Attempting to submit a second request for same entity must fail with ConflictError
    with pytest.raises(ConflictError):
        await service.submitForApproval(
            tenantId=tenant_id,
            entityType="BRAND",
            entityId=entity_id,
            operationType="UPDATE",
            versionData={"name": "Brand B"},
            submittedBy=user_id,
        )


@pytest.mark.asyncio
async def test_review_queue_management(testDb):
    """
    Verifies that ReviewQueue entry is auto-generated upon request submission,
    can be filtered, sorted, and assigned to platform staff.
    """
    service = ApprovalService(testDb)
    tenant_id = uuid.uuid4()
    entity_id = uuid.uuid4()
    user_id = uuid.uuid4()
    staff_id = uuid.uuid4()

    # Submit request -> review queue should get seeded
    req = await service.submitForApproval(
        tenantId=tenant_id,
        entityType="BRAND",
        entityId=entity_id,
        operationType="CREATE",
        versionData={"name": "Brand Alpha"},
        submittedBy=user_id,
    )

    # 1. Retrieve the review queue item
    queue_item = await service.queueRepo.getByApprovalRequestId(req.id)
    assert queue_item is not None
    assert queue_item.priority == "MEDIUM"
    assert queue_item.assignedTo is None

    # 2. Assign the queue item
    updated_queue = await service.queueRepo.update(queue_item, {"assignedTo": staff_id, "priority": "HIGH"})
    assert updated_queue.assignedTo == staff_id
    assert updated_queue.priority == "HIGH"

    # 3. Test list filter and sorting
    items, total = await service.queueRepo.listWithFilters(
        tenantId=tenant_id,
        entityType="BRAND",
        approvalStatus="PENDING",
        sortBy="priority",
        sortOrder="asc",
    )
    assert total == 1
    assert items[0].id == queue_item.id
    assert items[0].approvalRequest.entityType == "BRAND"


@pytest.mark.asyncio
async def test_approve_and_rejection_workflows(testDb):
    """
    Verifies workflow approval and publishing, rejection, and notification logging.
    """
    service = ApprovalService(testDb)
    tenant_id = uuid.uuid4()
    entity_id = uuid.uuid4()
    user_id = uuid.uuid4()
    reviewer_id = uuid.uuid4()

    # 1. Create a live Brand row so we can run updates on it
    live_brand = Brand(
        id=entity_id,
        tenantId=tenant_id,
        ownerStoreId=uuid.uuid4(),
        brandName="Brand Original",
        brandSlug="brand-original",
        verificationStatus="PENDING",
        isActive=True,
        createdBy=user_id,
    )
    testDb.add(live_brand)
    await testDb.flush()

    # 2. Submit change request to update the brand name
    updated_data = {
        "brandName": "Brand Approved Update",
        "brandSlug": "brand-approved-update",
        "verificationStatus": "APPROVED",
        "isActive": True,
    }
    req = await service.submitForApproval(
        tenantId=tenant_id,
        entityType="BRAND",
        entityId=entity_id,
        operationType="UPDATE",
        versionData=updated_data,
        submittedBy=user_id,
    )

    # 3. Approve the request
    approved_req = await service.approveRequest(
        requestId=req.id,
        reviewedBy=reviewer_id,
        remarks="LGTM",
    )
    assert approved_req.approvalStatus == "APPROVED"

    # 4. Verify live data is published (Publishing Engine)
    await testDb.refresh(live_brand)
    assert live_brand.brandName == "Brand Approved Update"

    # 5. Verify EntityVersion is marked as published
    pub_version = await service.versionRepo.getPublishedVersion("BRAND", entity_id)
    assert pub_version is not None
    assert pub_version.versionNumber == req.submittedVersionNumber
    assert pub_version.isPublished is True

    # 6. Verify queue item is deleted
    queue_item = await service.queueRepo.getByApprovalRequestId(req.id)
    assert queue_item is None

    # 7. Verify audit log entry
    audit_check = await testDb.execute(
        select(AuditLog).where(AuditLog.entityId == entity_id).where(AuditLog.actionType == "APPROVE")
    )
    audit = audit_check.scalar_one_or_none()
    assert audit is not None

    # 8. Test Rejection flow on a new request
    entity_id_2 = uuid.uuid4()
    req_reject = await service.submitForApproval(
        tenantId=tenant_id,
        entityType="BRAND",
        entityId=entity_id_2,
        operationType="CREATE",
        versionData={"brandName": "Rejected Brand"},
        submittedBy=user_id,
    )

    rejected_req = await service.rejectRequest(
        requestId=req_reject.id,
        reviewedBy=reviewer_id,
        rejectionReason="Logo document missing",
        remarks="Rejecting due to compliance details",
    )
    assert rejected_req.approvalStatus == "REJECTED"
    assert rejected_req.rejectionReason == "Logo document missing"

    # Verify notification log
    notif_check = await testDb.execute(
        select(AuditLog)
        .where(AuditLog.entityType == "APPROVAL_REQUEST")
        .where(AuditLog.entityId == req_reject.id)
        .where(AuditLog.actionType == "REJECT")
    )
    notif = notif_check.scalar_one_or_none()
    assert notif is not None
    assert notif.newValue["notification"] is True
    assert notif.newValue["targetUser"] == str(user_id)


@pytest.mark.asyncio
async def test_versioning_and_rollback(testDb):
    """
    Verifies that rolling back to a previous version restores live state
    and correctly creates a new version with audit trails.
    """
    service = ApprovalService(testDb)
    tenant_id = uuid.uuid4()
    entity_id = uuid.uuid4()
    user_id = uuid.uuid4()
    reviewer_id = uuid.uuid4()

    # 1. Create a live Brand row
    live_brand = Brand(
        id=entity_id,
        tenantId=tenant_id,
        ownerStoreId=uuid.uuid4(),
        brandName="Version 1",
        brandSlug="version-1",
        verificationStatus="APPROVED",
        isActive=True,
        createdBy=user_id,
    )
    testDb.add(live_brand)
    await testDb.flush()

    # Create a published EntityVersion representing the original state (Version 1)
    v1 = EntityVersion(
        tenantId=tenant_id,
        entityType="BRAND",
        entityId=entity_id,
        versionNumber=1,
        versionData={"brandName": "Version 1", "brandSlug": "version-1"},
        isPublished=True,
        createdBy=user_id,
    )
    testDb.add(v1)
    await testDb.flush()

    # 2. Submit change request for Version 2
    v2_data = {"brandName": "Version 2", "brandSlug": "version-2"}
    req = await service.submitForApproval(
        tenantId=tenant_id,
        entityType="BRAND",
        entityId=entity_id,
        operationType="UPDATE",
        versionData=v2_data,
        submittedBy=user_id,
    )
    await service.approveRequest(requestId=req.id, reviewedBy=reviewer_id)

    # Verify live Brand is now Version 2
    await testDb.refresh(live_brand)
    assert live_brand.brandName == "Version 2"

    # 3. Trigger rollback to Version 1 (using the version record ID)
    rolled_back_version = await service.rollbackEntity(
        versionId=v1.id,
        performedBy=user_id,
    )

    # 4. Verify live Brand is restored to Version 1
    await testDb.refresh(live_brand)
    assert live_brand.brandName == "Version 1"

    # 5. Verify a new published version was created (Version 3)
    assert rolled_back_version.versionNumber == 3
    assert rolled_back_version.isPublished is True
    assert rolled_back_version.versionData == {"brandName": "Version 1", "brandSlug": "version-1"}

    # 6. Verify audit log entry for RESTORE
    restore_audit = await testDb.execute(
        select(AuditLog).where(AuditLog.entityId == entity_id).where(AuditLog.actionType == "RESTORE")
    )
    audit = restore_audit.scalar_one_or_none()
    assert audit is not None
    assert audit.oldValue["brandName"] == "Version 2"
    assert audit.newValue["brandName"] == "Version 1"
