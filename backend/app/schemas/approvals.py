# Owner - pradhansaikat123@gmail.com
# Pydantic schemas for the Approval, Audit, and Versioning API.
# Coerces all inbound timezone-aware datetimes to naive datetimes for database compatibility.

# Import datetime and timezone for dealing with datetime records
from datetime import datetime, timezone
# Import IP address classes for network address type validation
from ipaddress import IPv4Address, IPv6Address
# Import types for standard dictionary, list, union, and optional annotations
from typing import Any, Dict, List, Optional, Union
# Import UUID class for typing database keys
from uuid import UUID
# Import BaseModel, validator decorators, and fields from Pydantic for schemas
from pydantic import BaseModel, Field, field_validator, model_validator


class SafeBaseModel(BaseModel):
    @model_validator(mode="after")
    def make_all_datetimes_naive(self) -> "SafeBaseModel":
        for fieldName, fieldValue in self.__dict__.items():
            if isinstance(fieldValue, datetime) and fieldValue.tzinfo is not None:
                self.__dict__[fieldName] = fieldValue.astimezone(timezone.utc).replace(tzinfo=None)
        return self


# ═══════════════════════════════════════════════
# APPROVAL REQUEST SCHEMAS
# ═══════════════════════════════════════════════
VALID_ENTITY_TYPES = {
    'STORE', 'SECTION', 'PRODUCT', 'SERVICE', 'BLOG', 'CATEGORY',
    'OFFER', 'POLICY', 'FORM', 'MEDIA', 'BRAND', 'CUSTOMER'
}

VALID_OPERATION_TYPES = {'CREATE', 'UPDATE', 'DELETE'}
VALID_APPROVAL_STATUSES = {'PENDING', 'APPROVED', 'REJECTED'}


class ApprovalRequestBase(SafeBaseModel):
    tenantId: UUID = Field(..., description="Tenant ID referencing tenant details")
    entityType: str = Field(..., description="Type of entity being modified")
    entityId: UUID = Field(..., description="ID of entity being modified")
    operationType: str = Field(..., description="CREATE, UPDATE, or DELETE")
    submittedVersionNumber: int = Field(..., description="Version of the entity awaiting approval")
    approvalStatus: str = Field(default="PENDING", description="Status of approval")
    submittedBy: UUID = Field(..., description="ID of user who submitted the request")
    remarks: Optional[str] = Field(default=None, description="Optional internal comments")

    @field_validator("entityType")
    @classmethod
    def validate_entity_type(cls, v):
        if v not in VALID_ENTITY_TYPES:
            raise ValueError(f"entityType must be one of {VALID_ENTITY_TYPES}")
        return v

    @field_validator("operationType")
    @classmethod
    def validate_operation_type(cls, v):
        if v not in VALID_OPERATION_TYPES:
            raise ValueError(f"operationType must be one of {VALID_OPERATION_TYPES}")
        return v

    @field_validator("approvalStatus")
    @classmethod
    def validate_approval_status(cls, v):
        if v not in VALID_APPROVAL_STATUSES:
            raise ValueError(f"approvalStatus must be one of {VALID_APPROVAL_STATUSES}")
        return v


class ApprovalRequestCreate(ApprovalRequestBase):
    pass


class ApprovalRequestUpdate(SafeBaseModel):
    approvalStatus: Optional[str] = Field(default=None, description="Set new approval status")
    reviewedBy: Optional[UUID] = Field(default=None, description="ID of the reviewing user")
    rejectionReason: Optional[str] = Field(default=None, description="Reason if request is rejected")
    remarks: Optional[str] = Field(default=None, description="Optional internal comments")

    @field_validator("approvalStatus")
    @classmethod
    def validate_approval_status(cls, v):
        if v is not None and v not in VALID_APPROVAL_STATUSES:
            raise ValueError(f"approvalStatus must be one of {VALID_APPROVAL_STATUSES}")
        return v


class ApprovalRequestResponse(ApprovalRequestBase):
    id: UUID
    submittedAt: datetime
    reviewedBy: Optional[UUID] = None
    reviewedAt: Optional[datetime] = None
    rejectionReason: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# APPROVAL REQUEST VERSION SCHEMAS
# ═══════════════════════════════════════════════
class ApprovalRequestVersionBase(SafeBaseModel):
    approvalRequestId: UUID = Field(..., description="Approval request ID referencing approvalRequests")
    versionNumber: int = Field(..., description="The snapshot version number")
    approvalStatus: str = Field(..., description="Status of this version's approval")
    reviewedBy: Optional[UUID] = Field(default=None, description="ID of the reviewer user")
    reviewComment: Optional[str] = Field(default=None, description="Comment on review decision")


class ApprovalRequestVersionCreate(ApprovalRequestVersionBase):
    pass


class ApprovalRequestVersionUpdate(SafeBaseModel):
    approvalStatus: Optional[str] = Field(default=None)
    reviewedBy: Optional[UUID] = Field(default=None)
    reviewComment: Optional[str] = Field(default=None)

    @field_validator("approvalStatus")
    @classmethod
    def validate_approval_status(cls, v):
        if v is not None and v not in VALID_APPROVAL_STATUSES:
            raise ValueError(f"approvalStatus must be one of {VALID_APPROVAL_STATUSES}")
        return v


class ApprovalRequestVersionResponse(ApprovalRequestVersionBase):
    id: UUID
    reviewedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# ENTITY VERSION SCHEMAS
# ═══════════════════════════════════════════════
class EntityVersionBase(SafeBaseModel):
    tenantId: UUID = Field(..., description="Tenant ID referencing tenant details")
    entityType: str = Field(..., description="Entity type, e.g. PRODUCT")
    entityId: UUID = Field(..., description="ID of the entity")
    versionNumber: int = Field(..., description="Incremental version number")
    versionData: Dict[str, Any] = Field(..., description="Complete snapshot data as a JSON object")
    isPublished: bool = Field(default=False, description="Is this version currently published")
    createdBy: UUID = Field(..., description="User ID who created this version")

    @field_validator("entityType")
    @classmethod
    def validate_entity_type(cls, v):
        if v not in VALID_ENTITY_TYPES:
            raise ValueError(f"entityType must be one of {VALID_ENTITY_TYPES}")
        return v


class EntityVersionCreate(EntityVersionBase):
    pass


class EntityVersionUpdate(SafeBaseModel):
    versionData: Optional[Dict[str, Any]] = Field(default=None)
    isPublished: Optional[bool] = Field(default=None)


class EntityVersionResponse(EntityVersionBase):
    id: UUID
    createdAt: datetime

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# AUDIT LOG SCHEMAS
# ═══════════════════════════════════════════════
VALID_ACTION_TYPES = {
    'CREATE', 'UPDATE', 'DELETE', 'RESTORE', 'LOGIN', 'LOGOUT',
    'APPROVE', 'REJECT', 'PAYMENT', 'REFUND', 'CANCEL', 'RETURN'
}


class AuditLogBase(SafeBaseModel):
    tenantId: Optional[UUID] = Field(default=None, description="Tenant ID (null for platform-level actions)")
    entityType: str = Field(..., description="Type of entity audited")
    entityId: UUID = Field(..., description="ID of entity audited")
    actionType: str = Field(..., description="Audit action type")
    oldValue: Optional[Union[Dict[str, Any], List[Any], str, int, float, bool]] = Field(default=None, description="Previous state snapshot")
    newValue: Optional[Union[Dict[str, Any], List[Any], str, int, float, bool]] = Field(default=None, description="New state snapshot")
    changedFields: Optional[Union[Dict[str, Any], List[Any], str, int, float, bool]] = Field(default=None, description="Differences/field level diff")
    performedBy: Optional[UUID] = Field(default=None, description="User ID performing the action")
    ipAddress: Optional[Union[IPv4Address, IPv6Address, str]] = Field(default=None, description="Client IP address")
    userAgent: Optional[str] = Field(default=None, description="Client User Agent string")

    @field_validator("actionType")
    @classmethod
    def validate_action_type(cls, v):
        if v not in VALID_ACTION_TYPES:
            raise ValueError(f"actionType must be one of {VALID_ACTION_TYPES}")
        return v


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogResponse(AuditLogBase):
    id: UUID
    createdAt: datetime

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# STATUS HISTORY SCHEMAS
# ═══════════════════════════════════════════════
VALID_STATUS_HISTORY_ENTITIES = {
    'PRODUCT', 'SERVICE', 'ORDER', 'BOOKING', 'CUSTOMER',
    'SHIPMENT', 'OFFER', 'STORE', 'BRAND', 'CATEGORY'
}


class StatusHistoryBase(SafeBaseModel):
    tenantId: UUID = Field(..., description="Tenant ID referencing tenant details")
    entityType: str = Field(..., description="Type of entity tracking status")
    entityId: UUID = Field(..., description="ID of entity tracking status")
    oldStatus: Optional[str] = Field(default=None, description="Status before transition")
    newStatus: str = Field(..., description="Status after transition")
    changeReason: Optional[str] = Field(default=None, description="Reason for status change")
    changedBy: UUID = Field(..., description="User ID who made this change")

    @field_validator("entityType")
    @classmethod
    def validate_entity_type(cls, v):
        if v not in VALID_STATUS_HISTORY_ENTITIES:
            raise ValueError(f"entityType must be one of {VALID_STATUS_HISTORY_ENTITIES}")
        return v


class StatusHistoryCreate(StatusHistoryBase):
    pass


class StatusHistoryResponse(StatusHistoryBase):
    """Response schema for status history records with system-generated fields."""
    id: UUID
    changedAt: datetime

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# WORKFLOW SCHEMAS (Change Requests, Approval, Rejection)
# ═══════════════════════════════════════════════

class DraftCreate(SafeBaseModel):
    """
    Schema for saving a draft of pending entity changes.
    Stores the entity snapshot without submitting for approval.
    """
    tenantId: UUID = Field(..., description="Tenant ID the draft belongs to")
    entityType: str = Field(..., description="Type of entity being modified (e.g. PRODUCT)")
    entityId: UUID = Field(..., description="ID of the entity being modified")
    versionData: Dict[str, Any] = Field(..., description="Complete snapshot of draft changes as JSON")
    createdBy: UUID = Field(..., description="User ID creating the draft")

    @field_validator("entityType")
    @classmethod
    def validate_entity_type(cls, v):
        """Validates entity type against allowed values."""
        if v not in VALID_ENTITY_TYPES:
            raise ValueError(f"entityType must be one of {VALID_ENTITY_TYPES}")
        return v


class RequestSubmit(SafeBaseModel):
    """
    Schema for submitting a change request for approval.
    Creates both an EntityVersion snapshot and an ApprovalRequest entry.
    """
    tenantId: UUID = Field(..., description="Tenant ID submitting the request")
    entityType: str = Field(..., description="Type of entity being submitted for approval")
    entityId: UUID = Field(..., description="ID of the entity being submitted")
    operationType: str = Field(..., description="CREATE, UPDATE, or DELETE")
    versionData: Dict[str, Any] = Field(..., description="Complete entity snapshot to be approved")
    submittedBy: UUID = Field(..., description="User ID submitting the request")
    remarks: Optional[str] = Field(default=None, description="Optional remarks for the reviewer")

    @field_validator("entityType")
    @classmethod
    def validate_entity_type(cls, v):
        """Validates entity type against allowed values."""
        if v not in VALID_ENTITY_TYPES:
            raise ValueError(f"entityType must be one of {VALID_ENTITY_TYPES}")
        return v

    @field_validator("operationType")
    @classmethod
    def validate_operation_type(cls, v):
        """Validates operation type against allowed values."""
        if v not in VALID_OPERATION_TYPES:
            raise ValueError(f"operationType must be one of {VALID_OPERATION_TYPES}")
        return v


class DraftUpdate(SafeBaseModel):
    """
    Schema for updating a pending draft's entity data.
    Only the versionData can be modified while a request is still PENDING.
    """
    versionData: Dict[str, Any] = Field(..., description="Updated entity snapshot data")


class ApprovePayload(SafeBaseModel):
    """
    Schema for approving a pending change request.
    Records the reviewer identity and optional remarks.
    """
    reviewedBy: UUID = Field(..., description="User ID of the reviewer approving the request")
    remarks: Optional[str] = Field(default=None, description="Optional approval remarks or notes")


class RejectPayload(SafeBaseModel):
    """
    Schema for rejecting a pending change request.
    Requires a rejection reason for audit trail purposes.
    """
    reviewedBy: UUID = Field(..., description="User ID of the reviewer rejecting the request")
    rejectionReason: str = Field(..., max_length=1000, description="Mandatory reason for rejection")
    remarks: Optional[str] = Field(default=None, description="Optional additional comments")


class RollbackPayload(SafeBaseModel):
    """
    Schema for rolling back an entity to a previous version.
    Records who performed the rollback operation.
    """
    performedBy: UUID = Field(..., description="User ID performing the rollback")


# ═══════════════════════════════════════════════
# REVIEW QUEUE SCHEMAS
# ═══════════════════════════════════════════════

VALID_PRIORITIES = {'HIGH', 'MEDIUM', 'LOW'}


class ReviewQueueCreate(SafeBaseModel):
    """
    Schema for creating a new review queue entry.
    Typically created automatically when a change request is submitted.
    """
    approvalRequestId: UUID = Field(..., description="FK to the approval request being queued")
    priority: str = Field(default="MEDIUM", description="Review priority: HIGH, MEDIUM, or LOW")
    notes: Optional[str] = Field(default=None, max_length=500, description="Optional notes for reviewer")

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v):
        """Validates priority value against allowed levels."""
        if v not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {VALID_PRIORITIES}")
        return v


class ReviewQueueAssign(SafeBaseModel):
    """
    Schema for assigning a review queue item to a platform staff member.
    """
    assignedTo: UUID = Field(..., description="User ID of the platform staff being assigned")


class ReviewQueueResponse(SafeBaseModel):
    """
    Response schema for review queue items.
    Includes the queue metadata and the linked approval request summary.
    """
    id: UUID
    approvalRequestId: UUID
    assignedTo: Optional[UUID] = None
    priority: str
    notes: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}

