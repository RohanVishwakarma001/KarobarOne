# Owner: mousamdas156@gmail.com
"""
================================================================================
STORE MODEL
================================================================================
Yeh file dukaano ki main metadata aur details (jaise naam, slug, email, logo) ko manage karti hai.
This model maps to the 'stores' table, representing a merchant storefront.

Why it is used:
- It serves as the primary root entity for storefronts.
- Links together sections, bank accounts, and social links under a single store ID.
================================================================================
"""

import uuid
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelWithUpdate


class Store(BaseModelWithUpdate):
    """
    ORM Model representing a Storefront/Website.
    Inherits UUID and full timestamps (created_at, updated_at).
    """
    __tablename__ = "stores"

    # ── Database Constraints ──────────────────────────────────────────
    __table_args__ = (
        # Ensure that the approval status is restricted to PENDING, APPROVED, or REJECTED
        CheckConstraint(
            "approval_status IN ('PENDING', 'APPROVED', 'REJECTED')",
            name="ck_stores_approval_status",
        ),
    )

    # Foreign key pointing to the merchant Tenant who owns this store
    tenantId: Mapped[uuid.UUID] = mapped_column(
        "tenant_id",
        UUID(as_uuid=True),
        ForeignKey("tenants_details.id"),
        nullable=False,
    )

    # Display name of the store (e.g. "My Fashion Hub")
    storeName: Mapped[str] = mapped_column(
        "store_name",
        String(150),
        nullable=False,
    )

    # Unique URL-friendly identifier of the store (e.g. "my-fashion-hub"). Used for routing.
    storeSlug: Mapped[str] = mapped_column(
        "store_slug",
        String(100),
        unique=True,
        nullable=False,
    )

    # Short marketing tagline for the store
    tagline: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Official contact email address of the store
    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Contact phone number of the store
    mobile: Mapped[str | None] = mapped_column(
        String(15),
        nullable=True,
    )

    # WhatsApp support phone number of the store
    whatsappMobile: Mapped[str | None] = mapped_column(
        "whatsapp_mobile",
        String(15),
        nullable=True,
    )

    # Detailed rich text or plain text description of the store's business
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Foreign key referencing the store's uploaded Logo image in media files
    logoMediaId: Mapped[uuid.UUID | None] = mapped_column(
        "logo_media_id",
        UUID(as_uuid=True),
        ForeignKey("media_files.id"),
        nullable=True,
    )

    # Foreign key referencing the store's browser Favicon icon in media files
    faviconMediaId: Mapped[uuid.UUID | None] = mapped_column(
        "favicon_media_id",
        UUID(as_uuid=True),
        ForeignKey("media_files.id"),
        nullable=True,
    )

    # Foreign key referencing the store's Hero Banner image in media files
    heroMediaId: Mapped[uuid.UUID | None] = mapped_column(
        "hero_media_id",
        UUID(as_uuid=True),
        ForeignKey("media_files.id"),
        nullable=True,
    )

    # Flag to enable/disable the storefront website publicly
    isActive: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        default=True,
        nullable=False,
    )

    # Admin approval status (determines if the store is verified for publishing)
    approvalStatus: Mapped[str] = mapped_column(
        "approval_status",
        String(20),
        default="DRAFT",
        nullable=False,
    )

    # ── Relationships ──────────────────────────────────────────────────
    # Link to associated bank accounts. Cascade delete ensures bank records are cleaned up when the store is deleted.
    bankAccounts = relationship(
        "StoreBankAccount",
        back_populates="store",
        cascade="all, delete-orphan",
    )

    # Link to associated website layout sections.
    sections = relationship(
        "Section",
        back_populates="store",
        cascade="all, delete-orphan",
    )

    # Link to social media profiles.
    socialLinks = relationship(
        "SocialLink",
        back_populates="store",
        cascade="all, delete-orphan",
    )


    websiteSettings = relationship(
        "WebsiteSetting",
        back_populates="store",
        cascade="all, delete-orphan",
        uselist=False,
    )

    deployments = relationship(
        "WebsiteDeployment",
        back_populates="store",
        cascade="all, delete-orphan",
    )

    publishLogs = relationship(
        "WebsitePublishLog",
        back_populates="store",
        cascade="all, delete-orphan",
    )

    aiContents = relationship(
        "WebsiteAIContent",
        back_populates="store",
        cascade="all, delete-orphan",
    )

# Website module relationships

websiteSettings = relationship(
    "WebsiteSetting",
    back_populates="store",
    cascade="all, delete-orphan",
)

deployments = relationship(
    "WebsiteDeployment",
    back_populates="store",
    cascade="all, delete-orphan",
)

publishLogs = relationship(
    "WebsitePublishLog",
    back_populates="store",
    cascade="all, delete-orphan",
)

aiContents = relationship(
    "WebsiteAIContent",
    back_populates="store",
    cascade="all, delete-orphan",
)
