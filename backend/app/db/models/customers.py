# Owner - pradhansaikat123@gmail.com
# SQLAlchemy database models for Customer Management. Defines tables, relationships,
# and constraints for customers, addresses, sessions, notes, groups, and consent records.

import uuid  # For UUID generation
from datetime import datetime  # For handling timestamp values

from sqlalchemy import (
    Boolean,  # For boolean columns (e.g. is_default, active status)
    CheckConstraint,  # For checking valid column values (e.g. status enum)
    Column,  # For defining database columns
    ForeignKey,  # For defining relation links between tables
    SmallInteger,  # For small integer numbers (e.g. attempt counters)
    String,  # For string/varchar fields (e.g. email, names)
    Text,  # For long text fields (e.g. note description)
    UniqueConstraint,  # For establishing multi-column unique indices
)
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID  # Postgres specific column types
from sqlalchemy.orm import relationship  # For ORM relationship linkages
from sqlalchemy.sql import func  # For database functions (e.g. current timestamp)
from sqlalchemy.types import TIMESTAMP  # For timestamp fields in database

from app.db.base import Base  # Declarative base class for models


def gen_uuid():
    return str(uuid.uuid4())


# ─────────────────────────────────────────────
# customers
# ─────────────────────────────────────────────
class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = (
        UniqueConstraint("store_id", "email", name="uq_customers_store_email"),
        UniqueConstraint("store_id", "mobile", name="uq_customers_store_mobile"),
        CheckConstraint(
            "status IN ('ACTIVE','INACTIVE','BLOCKED')", name="ck_customers_status"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    storeId = Column("store_id", UUID(as_uuid=True), nullable=False)
    customerCode = Column("customer_code", String(30), unique=True, nullable=False)
    firstName = Column("first_name", String(100), nullable=False)
    lastName = Column("last_name", String(100), nullable=True)
    email = Column(String(255), nullable=False)
    mobile = Column(String(15), nullable=False)
    passwordHash = Column("password_hash", String(255), nullable=True)
    status = Column(String(20), nullable=False, default="ACTIVE")
    isGuestCustomer = Column("is_guest_customer", Boolean, default=False)
    isEmailVerified = Column("is_email_verified", Boolean, default=False)
    isMobileVerified = Column("is_mobile_verified", Boolean, default=False)
    lastLoginAt = Column("last_login_at", TIMESTAMP, nullable=True)
    registeredAt = Column("registered_at", TIMESTAMP, server_default=func.now())
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deletedAt = Column("deleted_at", TIMESTAMP, nullable=True)

    addresses = relationship("CustomerAddress", back_populates="customer", lazy="selectin")
    sessions = relationship("CustomerSession", back_populates="customer")
    activityLogs = relationship("CustomerActivityLog", back_populates="customer")
    groupMemberships = relationship("CustomerGroupMember", back_populates="customer")
    notes = relationship("CustomerNote", back_populates="customer")
    consentLogs = relationship("CustomerConsentLog", back_populates="customer")
    passwordResetTokens = relationship("CustomerPasswordResetToken", back_populates="customer")


# ─────────────────────────────────────────────
# customerAddresses
# ─────────────────────────────────────────────
class CustomerAddress(Base):
    # Real table is camelCase ("customerAddresses") — every other
    # customer_* table is snake_case; this one and CustomerSession below
    # were provisioned with a naming typo. Columns inside are correctly
    # snake_case (verified against information_schema), just the table name.
    __tablename__ = "customerAddresses"
    __table_args__ = (
        CheckConstraint(
            "address_type IN ('SHIPPING','BILLING')", name="ck_address_type"
        ),
        {"extend_existing": True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customerId = Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    addressType = Column("address_type", String(20), nullable=False)
    fullName = Column("full_name", String(150), nullable=False)
    mobile = Column(String(15), nullable=False)
    addressLine1 = Column("address_line_1", String(255), nullable=False)
    addressLine2 = Column("address_line_2", String(255), nullable=True)
    landmark = Column(String(150), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False, default="India")
    postalCode = Column("postal_code", String(10), nullable=False)
    isDefault = Column("is_default", Boolean, default=False)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="addresses")


# ─────────────────────────────────────────────
# customerSessions
# ─────────────────────────────────────────────
class CustomerSession(Base):
    # See the matching note on CustomerAddress above — real table is "customerSessions".
    __tablename__ = "customerSessions"
    __table_args__ = (
        {"extend_existing": True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customerId = Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    refreshTokenHash = Column("refresh_token_hash", String(255), nullable=False)
    ipAddress = Column("ip_address", INET, nullable=True)
    userAgent = Column("user_agent", String(1000), nullable=True)
    loginAt = Column("login_at", TIMESTAMP, nullable=False)
    logoutAt = Column("logout_at", TIMESTAMP, nullable=True)
    expiresAt = Column("expires_at", TIMESTAMP, nullable=False)
    isActive = Column("is_active", Boolean, default=True)

    customer = relationship("Customer", back_populates="sessions")


# ─────────────────────────────────────────────
# customer_activity_logs
# ─────────────────────────────────────────────
class CustomerActivityLog(Base):
    __tablename__ = "customer_activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customerId = Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    activityType = Column("activity_type", String(50), nullable=False)
    entityType = Column("entity_type", String(50), nullable=True)
    entityId = Column("entity_id", UUID(as_uuid=True), nullable=True)
    activityData = Column("activity_data", JSONB, nullable=True)
    ipAddress = Column("ip_address", INET, nullable=True)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())

    customer = relationship("Customer", back_populates="activityLogs")


# ─────────────────────────────────────────────
# customer_groups
# ─────────────────────────────────────────────
class CustomerGroup(Base):
    __tablename__ = "customer_groups"
    __table_args__ = (
        UniqueConstraint("store_id", "group_name", name="uq_groups_store_name"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    storeId = Column("store_id", UUID(as_uuid=True), nullable=False)
    groupName = Column("group_name", String(100), nullable=False)
    description = Column(String(500), nullable=True)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())

    members = relationship("CustomerGroupMember", back_populates="group")


# ─────────────────────────────────────────────
# customer_group_members
# ─────────────────────────────────────────────
class CustomerGroupMember(Base):
    __tablename__ = "customer_group_members"
    __table_args__ = (
        UniqueConstraint("customer_id", "group_id", name="uq_group_member"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customerId = Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    groupId = Column("group_id", UUID(as_uuid=True), ForeignKey("customer_groups.id"), nullable=False)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())

    customer = relationship("Customer", back_populates="groupMemberships")
    group = relationship("CustomerGroup", back_populates="members")


# ─────────────────────────────────────────────
# customer_notes
# ─────────────────────────────────────────────
class CustomerNote(Base):
    __tablename__ = "customer_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customerId = Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    noteText = Column("note_text", Text, nullable=False)
    createdBy = Column("created_by", UUID(as_uuid=True), nullable=False)  # FK → users.id
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())

    customer = relationship("Customer", back_populates="notes")


# ─────────────────────────────────────────────
# customer_consent_logs
# ─────────────────────────────────────────────
class CustomerConsentLog(Base):
    __tablename__ = "customer_consent_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customerId = Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    consentType = Column("consent_type", String(50), nullable=False)
    accepted = Column(Boolean, nullable=False)
    ipAddress = Column("ip_address", INET, nullable=True)
    acceptedAt = Column("accepted_at", TIMESTAMP, nullable=False)

    customer = relationship("Customer", back_populates="consentLogs")


# ─────────────────────────────────────────────
# customer_password_reset_tokens
# ─────────────────────────────────────────────
class CustomerPasswordResetToken(Base):
    __tablename__ = "customer_password_reset_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customerId = Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    tokenHash = Column("token_hash", String(255), nullable=False)
    expiresAt = Column("expires_at", TIMESTAMP, nullable=False)
    usedAt = Column("used_at", TIMESTAMP, nullable=True)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())

    customer = relationship("Customer", back_populates="passwordResetTokens")


# ─────────────────────────────────────────────
# guest_checkout_logs
# ─────────────────────────────────────────────
class GuestCheckoutLog(Base):
    __tablename__ = "guest_checkout_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    storeId = Column("store_id", UUID(as_uuid=True), nullable=False)
    customerId = Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    orderId = Column("order_id", UUID(as_uuid=True), nullable=True)
    bookingId = Column("booking_id", UUID(as_uuid=True), nullable=True)
    guestName = Column("guest_name", String(150), nullable=False)
    guestEmail = Column("guest_email", String(255), nullable=False)
    guestMobile = Column("guest_mobile", String(15), nullable=False)
    guestAddressJson = Column("guest_address_json", JSONB, nullable=True)
    convertedToCustomer = Column("converted_to_customer", Boolean, default=False)
    convertedAt = Column("converted_at", TIMESTAMP, nullable=True)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())


# ─────────────────────────────────────────────
# entity_verifications
# ─────────────────────────────────────────────
class EntityVerification(Base):
    __tablename__ = "entity_verifications"
    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('CUSTOMER','ORDER','BOOKING')",
            name="ck_entity_type",
        ),
        CheckConstraint(
            "verification_type IN ('EMAIL','MOBILE','ORDER_CONFIRMATION','BOOKING_CONFIRMATION')",
            name="ck_verification_type",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityType = Column("entity_type", String(30), nullable=False)
    entityId = Column("entity_id", UUID(as_uuid=True), nullable=False)
    verificationType = Column("verification_type", String(30), nullable=False)
    otpHash = Column("otp_hash", String(255), nullable=False)
    expiresAt = Column("expires_at", TIMESTAMP, nullable=False)
    verifiedAt = Column("verified_at", TIMESTAMP, nullable=True)
    attempts = Column(SmallInteger, default=0)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
