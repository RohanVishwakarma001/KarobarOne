# Owner - pradhansaikat123@gmail.com
# SQLAlchemy database models for Approval, Audit, and Versioning. Defines tables, relationships,
# and constraints for approval requests, request versions, entity versions, audit logs, and status history.

# Import standard uuid library for generating unique IDs
import uuid
# Import standard SQLAlchemy columns, constraints, and column structures
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
# Import PostgreSQL-specific column types (network address, JSON type, database UUID)
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID
# Import relationship construct to manage database mappings between related tables
from sqlalchemy.orm import relationship
# Import func to invoke SQL functions like NOW() dynamically
from sqlalchemy.sql import func
# Import TIMESTAMP column type for storing timestamps
from sqlalchemy.types import TIMESTAMP
# Import declarative Base class to associate models with a single metadata registry
from app.db.base import Base


# ─────────────────────────────────────────────
# approval_requests
# ─────────────────────────────────────────────
class ApprovalRequest(Base):
    # Real table is camelCase ("approvalRequests") — same tablename-typo
    # pattern as AuditLog/StatusHistory/CustomerAddress/CustomerSession
    # elsewhere in this codebase, all fixed the same way. Every query
    # against this model has always raised UndefinedTableError until now.
    __tablename__ = "approvalRequests"
    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('STORE','SECTION','PRODUCT','SERVICE','BLOG','CATEGORY','OFFER','POLICY','FORM','MEDIA','BRAND','CUSTOMER')",
            name="ck_approvalRequests_entity_type"
        ),
        CheckConstraint(
            "operation_type IN ('CREATE','UPDATE','DELETE')",
            name="ck_approvalRequests_operation_type"
        ),
        CheckConstraint(
            "approval_status IN ('PENDING','APPROVED','REJECTED')",
            name="ck_approvalRequests_approval_status"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False, index=True)
    entityType = Column("entity_type", String(50), nullable=False, index=True)
    entityId = Column("entity_id", UUID(as_uuid=True), nullable=False, index=True)
    operationType = Column("operation_type", String(20), nullable=False)
    submittedVersionNumber = Column("submitted_version_number", Integer, nullable=False)
    approvalStatus = Column("approval_status", String(20), nullable=False, default="PENDING", index=True)
    submittedBy = Column("submitted_by", UUID(as_uuid=True), nullable=False)  # FK → users.id
    submittedAt = Column("submitted_at", TIMESTAMP, nullable=False, server_default=func.now(), index=True)
    reviewedBy = Column("reviewed_by", UUID(as_uuid=True), nullable=True)  # FK → users.id
    reviewedAt = Column("reviewed_at", TIMESTAMP, nullable=True)
    rejectionReason = Column("rejection_reason", String(1000), nullable=True)
    remarks = Column("remarks", String(1000), nullable=True)
    createdAt = Column("created_at", TIMESTAMP, nullable=False, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    versions = relationship(
        "ApprovalRequestVersion",
        back_populates="approvalRequest",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


# ─────────────────────────────────────────────
# approval_request_versions
# ─────────────────────────────────────────────
class ApprovalRequestVersion(Base):
    __tablename__ = "approval_request_versions"
    __table_args__ = (
        UniqueConstraint("approval_request_id", "version_number", name="uq_approval_request_version"),
        CheckConstraint(
            "approval_status IN ('PENDING','APPROVED','REJECTED')",
            name="ck_approval_request_versions_approval_status"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    approvalRequestId = Column("approval_request_id", UUID(as_uuid=True), ForeignKey("approvalRequests.id"), nullable=False)
    versionNumber = Column("version_number", Integer, nullable=False)
    approvalStatus = Column("approval_status", String(20), nullable=False)
    reviewedBy = Column("reviewed_by", UUID(as_uuid=True), nullable=True)  # FK → users.id
    reviewComment = Column("review_comment", String(2000), nullable=True)
    reviewedAt = Column("reviewed_at", TIMESTAMP, server_default=func.now())

    approvalRequest = relationship("ApprovalRequest", back_populates="versions")


# ─────────────────────────────────────────────
# entity_versions
# ─────────────────────────────────────────────
class EntityVersion(Base):
    # See the matching note on ApprovalRequest above — real table is "entityVersions".
    __tablename__ = "entityVersions"
    __table_args__ = (
        UniqueConstraint("entity_type", "entity_id", "version_number", name="uq_entity_version_number"),
        CheckConstraint(
            "entity_type IN ('STORE','SECTION','PRODUCT','SERVICE','BLOG','CATEGORY','OFFER','POLICY','FORM','MEDIA','BRAND','CUSTOMER')",
            name="ck_entityVersions_entity_type"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    entityType = Column("entity_type", String(50), nullable=False, index=True)
    entityId = Column("entity_id", UUID(as_uuid=True), nullable=False, index=True)
    versionNumber = Column("version_number", Integer, nullable=False)
    versionData = Column("version_data", JSONB, nullable=False)
    isPublished = Column("is_published", Boolean, default=False)
    createdBy = Column("created_by", UUID(as_uuid=True), nullable=False)  # FK → users.id
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now(), index=True)


# ─────────────────────────────────────────────
# audit_logs
# ─────────────────────────────────────────────
class AuditLog(Base):
    # Real table is camelCase ("auditLogs") — this snake_case name has never
    # matched, meaning every AuditLog() insert anywhere in the app has always
    # raised UndefinedTableError (confirmed live; see
    # app/productsPorted/routers/products.py's audit-log try/except blocks,
    # added defensively before this root cause was found). Fixing here makes
    # audit logging actually work everywhere it's already wired, not just there.
    __tablename__ = "auditLogs"
    __table_args__ = (
        CheckConstraint(
            "action_type IN ('CREATE','UPDATE','DELETE','RESTORE','LOGIN','LOGOUT','APPROVE','REJECT','PAYMENT','REFUND','CANCEL','RETURN')",
            name="ck_auditLogs_action_type"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=True)
    entityType = Column("entity_type", String(50), nullable=False, index=True)
    entityId = Column("entity_id", UUID(as_uuid=True), nullable=False, index=True)
    actionType = Column("action_type", String(50), nullable=False)
    oldValue = Column("old_value", JSONB, nullable=True)
    newValue = Column("new_value", JSONB, nullable=True)
    changedFields = Column("changed_fields", JSONB, nullable=True)
    performedBy = Column("performed_by", UUID(as_uuid=True), nullable=True, index=True)  # FK → users.id
    ipAddress = Column("ip_address", INET, nullable=True)
    userAgent = Column("user_agent", Text, nullable=True)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now(), index=True)


# ─────────────────────────────────────────────
# status_history
# ─────────────────────────────────────────────
class StatusHistory(Base):
    # See the matching note on AuditLog above — real table is "statusHistory".
    __tablename__ = "statusHistory"
    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('PRODUCT','SERVICE','ORDER','BOOKING','CUSTOMER','SHIPMENT','OFFER','STORE','BRAND','CATEGORY')",
            name="ck_statusHistory_entity_type"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    entityType = Column("entity_type", String(50), nullable=False, index=True)
    entityId = Column("entity_id", UUID(as_uuid=True), nullable=False, index=True)
    oldStatus = Column("old_status", String(50), nullable=True)
    newStatus = Column("new_status", String(50), nullable=False)
    changeReason = Column("change_reason", String(500), nullable=True)
    changedBy = Column("changed_by", UUID(as_uuid=True), nullable=False)  # FK → users.id
    changedAt = Column("changed_at", TIMESTAMP, server_default=func.now(), index=True)


# ─────────────────────────────────────────────
# review_queue
# ─────────────────────────────────────────────
class ReviewQueue(Base):
    """
    Review queue table for tracking approval request assignments.
    Each approval request can have at most one queue entry (UNIQUE constraint).
    Platform staff are assigned via the assignedTo field.
    Priority levels (HIGH, MEDIUM, LOW) control review ordering.
    """
    # Unlike its siblings above, this table doesn't exist yet under EITHER
    # naming convention ("review_queue" or "reviewQueue" — checked live) —
    # not a tablename typo this time, just never created. Named camelCase to
    # match every other table in this approval/audit subsystem
    # (approvalRequests, entityVersions, auditLogs, statusHistory).
    __tablename__ = "reviewQueue"
    __table_args__ = (
        UniqueConstraint("approval_request_id", name="uq_review_queue_approval_request"),
        CheckConstraint(
            "priority IN ('HIGH','MEDIUM','LOW')",
            name="ck_reviewQueue_priority"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    approvalRequestId = Column(
        "approval_request_id", UUID(as_uuid=True),
        ForeignKey("approvalRequests.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    assignedTo = Column("assigned_to", UUID(as_uuid=True), nullable=True, index=True)  # FK → users.id
    priority = Column("priority", String(20), nullable=False, default="MEDIUM")
    notes = Column("notes", String(500), nullable=True)
    createdAt = Column("created_at", TIMESTAMP, nullable=False, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    approvalRequest = relationship("ApprovalRequest", lazy="selectin")
