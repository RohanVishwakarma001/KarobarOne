# Owner: mousamdas156@gmail.com
import uuid
from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelWithUpdate


# --------------------------------------------------------------------------------
# Tenant Model
# Houses the registration, address, status, and KYC verification details of SaaS tenants.
# Uses 'BaseModelWithUpdate' to automatically populate both createdAt and updatedAt.
# --------------------------------------------------------------------------------
class Tenant(BaseModelWithUpdate):
    __tablename__ = "tenants_details"

    # Index: Composite index on city and state to speed up query performance.
    # CheckConstraint: Prevents negative employee counts at the database level.
    __table_args__ = (
        Index("idx_tenant_city_state", "city", "state"),
        CheckConstraint(
            "employeeCount >= 0",
            name="ck_employee_count_positive",
        ),
    )

    # ---------- Basic Information ----------

    # gstNumber: Unique 15-character Goods and Services Tax Identification Number (optional)
    gstNumber: Mapped[str | None] = mapped_column(
        "gst_number",
        String(15),
        unique=True,
        nullable=True,
    )
    # panNumber: Mandatory unique Permanent Account Number (10-character code)
    panNumber: Mapped[str] = mapped_column(
        "pan_number",
        String(10),
        unique=True,
        nullable=False,
    )
    # documentMediaLink: Cloud storage link (S3/GCS) containing verification documents
    documentMediaLink: Mapped[str | None] = mapped_column(
        "document_media_link",
        Text,
        nullable=True,
    )
    # documentVerificationDone: True if verification checks are completed
    documentVerificationDone: Mapped[bool] = mapped_column(
        "document_verification_done",
        Boolean,
        default=False,
        nullable=False,
    )
    # documentVerificationDoneBy: User UUID of the internal staff who verified the tenant
    documentVerificationDoneBy: Mapped[uuid.UUID | None] = mapped_column(
        "document_verification_done_by",
        UUID(as_uuid=True),
        nullable=True,
    )
    # documentVerificationDoneAt: Timestamp when verification took place
    documentVerificationDoneAt: Mapped[datetime | None] = mapped_column(
        "document_verification_done_at",
        DateTime(timezone=True),
        nullable=True,
    )
    # businessName: Public-facing brand name of the business
    businessName: Mapped[str] = mapped_column(
        "business_name",
        String(255),
        nullable=False,
    )
    # legalName: Officially registered legal name of the entity
    legalName: Mapped[str] = mapped_column(
        "legal_name",
        String(255),
        nullable=False,
    )
    # logoMediaId: Foreign Key pointing to media/logo storage assets (optional)
    logoMediaId: Mapped[uuid.UUID | None] = mapped_column(
        "logo_media_id",
        UUID(as_uuid=True),
        nullable=True,
    )
    # email: Primary billing/owner email for communicating with the tenant
    email: Mapped[str] = mapped_column(
        "email",
        String(255),
        unique=True,
        nullable=False,
    )
    # mobile: Primary E.164 formatted contact number of the tenant
    mobile: Mapped[str] = mapped_column(
        "mobile",
        String(15),
        unique=True,
        nullable=False,
    )
    # whatsappMobile: Optional contact number dedicated for business messages
    whatsappMobile: Mapped[str | None] = mapped_column(
        "whatsapp_mobile",
        String(15),
        nullable=True,
    )
    # ownerName: Name of the primary tenant contact or business owner
    ownerName: Mapped[str] = mapped_column(
        "owner_name",
        String(150),
        nullable=False,
    )

    # ---------- Address Details ----------

    businessAddressLine1: Mapped[str] = mapped_column(
        "business_address_line1",
        String(255),
        nullable=False,
    )
    businessAddressLine2: Mapped[str | None] = mapped_column(
        "business_address_line2",
        String(255),
        nullable=True,
    )
    # locationLatitude: Precision GPS coordinate mapping
    locationLatitude: Mapped[Decimal | None] = mapped_column(
        "location_latitude",
        Numeric(10, 7),
        nullable=True,
    )
    # locationLongitude: Precision GPS coordinate mapping
    locationLongitude: Mapped[Decimal | None] = mapped_column(
        "location_longitude",
        Numeric(10, 7),
        nullable=True,
    )
    landmark: Mapped[str | None] = mapped_column(
        "landmark",
        String(150),
        nullable=True,
    )
    postOffice: Mapped[str | None] = mapped_column(
        "post_office",
        String(100),
        nullable=True,
    )
    policeStation: Mapped[str | None] = mapped_column(
        "police_station",
        String(100),
        nullable=True,
    )
    city: Mapped[str] = mapped_column(
        "city",
        String(100),
        nullable=False,
    )
    state: Mapped[str] = mapped_column(
        "state",
        String(100),
        nullable=False,
    )
    country: Mapped[str] = mapped_column(
        "country",
        String(100),
        default="India",
        server_default="India",
        nullable=False,
    )
    postalCode: Mapped[str] = mapped_column(
        "postal_code",
        String(10),
        nullable=False,
    )

    # ---------- Business Domain / Metadata ----------

    # businessType: Category description (e.g., 'Retail', 'Wholesale', 'Service')
    businessType: Mapped[str] = mapped_column(
        "business_type",
        String(100),
        nullable=False,
    )
    businessDescription: Mapped[str | None] = mapped_column(
        "business_description",
        Text,
        nullable=True,
    )
    employeeCount: Mapped[int | None] = mapped_column(
        "employee_count",
        Integer,
        nullable=True,
    )
    # registeredAt: Official business incorporation date/time
    registeredAt: Mapped[datetime | None] = mapped_column(
        "registered_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # ---------- Status & Active State (Computed / Properties) ----------
    @property
    def statusId(self):
        return getattr(self, "_statusId", 1)

    @statusId.setter
    def statusId(self, value):
        self._statusId = value

    @property
    def isActive(self):
        return getattr(self, "_isActive", True)

    @isActive.setter
    def isActive(self, value):
        self._isActive = value

    # ---------- Relationships ----------

    @property
    def status(self):
        return None
    
    settings = relationship(
        "TenantSettings",
        back_populates="tenant",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # planMapping: One-to-one link to active subscription plan config.
    # cascade="all, delete-orphan" removes plan mapping if tenant is deleted.
    planMapping = relationship(
        "TenantPlanMapping",
        back_populates="tenant",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # domains: Subdomains and custom domains linked to this tenant.
    domains = relationship(
        "TenantDomainMapping",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    # planHistory: Persistent history records of plan upgrades, downgrades or cancellations.
    planHistory = relationship(
        "TenantPlanHistory",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )