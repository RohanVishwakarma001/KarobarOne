# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA UPLOAD LOG ORM MODEL (mediaUploadLog.py)
================================================================================
Why this file is used:
- This file defines the `MediaUploadLog` database model mapping to the 'media_upload_logs' table.
- It acts as an audit trail log, tracking every lifecycle event (upload, update, delete, etc.)
  performed on any media file by system users, including history changes.
================================================================================
"""

# Standard library imports for UUIDs and generic dynamic types
import uuid
from typing import Any

# Third-party SQLAlchemy schema, JSON types, and relationships
from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Custom base model that provides ID and createdAt fields
from app.db.base import BaseModelCreated as BaseModel


class MediaUploadLog(BaseModel):
    """
    ORM Model representing an audit log entry for operations performed on media files.
    Inherits primary key UUID and createdAt timestamp from BaseModel.
    """
    __tablename__ = "media_upload_logs"

    # Restrict the action type using a CHECK constraint
    __table_args__ = (
        CheckConstraint(
            "action_type IN ('UPLOAD', 'UPDATE', 'DELETE', 'RESTORE', 'METADATA_UPDATE')",
            name="ck_media_upload_logs_action_type",
        ),
    )

    # Reference to the target media file
    mediaFileId: Mapped[uuid.UUID] = mapped_column(
        "media_file_id",
        UUID(as_uuid=True),
        ForeignKey("media_files.id"),
        nullable=False,
    )

    # The type of activity performed (e.g. 'UPLOAD')
    actionType: Mapped[str] = mapped_column(
        "action_type",
        String(50),
        nullable=False,
    )

    # Reference to the system User who triggered the action
    performedBy: Mapped[uuid.UUID] = mapped_column(
        "performed_by",
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # JSON snapshot representation of the old entity properties (before update/delete)
    oldValue: Mapped[dict[str, Any] | None] = mapped_column(
        "old_value",
        JSONB,
        nullable=True,
    )

    # JSON snapshot representation of the new entity properties (after upload/update)
    newValue: Mapped[dict[str, Any] | None] = mapped_column(
        "new_value",
        JSONB,
        nullable=True,
    )

    # ── ORM Relationships ──────────────────────────────────────────────────
    
    # Reference back to parent MediaFile
    mediaFile = relationship(
        "MediaFile",
        back_populates="uploadLogs",
    )
