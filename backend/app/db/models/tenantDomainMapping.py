# Owner: mousamdas156@gmail.com
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated as BaseModel


# --------------------------------------------------------------------------------
# TenantDomainMapping Model
# Maps specific subdomains (e.g. tenantname.karobar.com) or custom domains
# (e.g. www.tenantbusiness.in) to SaaS tenants.
# Uses 'BaseModel' to automatically include a 'createdAt' timestamp.
# --------------------------------------------------------------------------------
class TenantDomainMapping(BaseModel):
    __tablename__ = "tenant_domain_mapping"

    # check_domain_required: Assures either subDomain or customDomain (or both) are filled.
    __table_args__ = (
        CheckConstraint(
            "(sub_domain IS NOT NULL) OR (custom_domain IS NOT NULL)",
            name="ck_domain_required",
        ),
    )

    # tenantId: The tenant matching these domain routing rules.
    # ondelete="CASCADE" automatically cleans domain routing rules if the tenant is deleted.
    tenantId: Mapped[uuid.UUID] = mapped_column(
        "tenant_id",
        UUID(as_uuid=True),
        ForeignKey(
            "tenants_details.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # domainType: E.g., 'SUBDOMAIN' or 'CUSTOM' (helps identify route mapping type)
    domainType: Mapped[str] = mapped_column(
        "domain_type",
        String(20),
        nullable=False,
    )

    # subDomain: Standard platform subdomain (must be globally unique)
    subDomain: Mapped[str | None] = mapped_column(
        "sub_domain",
        String(100),
        unique=True,
        nullable=True,
    )

    # customDomain: Tenant's own external custom domain URL (must be globally unique)
    customDomain: Mapped[str | None] = mapped_column(
        "custom_domain",
        String(255),
        unique=True,
        nullable=True,
    )

    # isPrimary: Indicates if this is the primary entry-point URL for their web application
    isPrimary: Mapped[bool] = mapped_column(
        "is_primary",
        Boolean,
        default=False,
        nullable=False,
    )

    # DNS verification state for custom domains.
    dnsVerified: Mapped[bool] = mapped_column(
        "dns_verified",
        Boolean,
        default=False,
        nullable=False,
    )

    dnsVerificationToken: Mapped[str | None] = mapped_column(
        "dns_verification_token",
        String(255),
        nullable=True,
    )

    # sslExpiry: Tracks Let's Encrypt / external certificate expiry date for automatic renewals
    sslExpiry: Mapped[datetime | None] = mapped_column(
        "ssl_expiry",
        DateTime(timezone=True),
        nullable=True,
    )

    # tenant: Relationship back to the related Tenant record.
    tenant = relationship(
        "Tenant",
        back_populates="domains",
    )