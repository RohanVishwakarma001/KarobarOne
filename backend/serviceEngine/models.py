# Owner-pradhansaikat123@gmail.com

import uuid
from datetime import datetime, time
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    Numeric,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    JSON,
    SmallInteger,
    TypeDecorator,
    Time,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.db.base import Base

# Import the existing Category model as ServiceCategory alias to avoid SQLAlchemy metadata table duplication conflicts
from app.db.models.categories import Category as ServiceCategory

class ServiceTypeInteger(TypeDecorator):
    impl = SmallInteger
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value == "PHYSICAL":
            return 1
        elif value == "ONLINE":
            return 2
        return 1

    def process_result_value(self, value, dialect):
        if value == 1:
            return "PHYSICAL"
        elif value == 2:
            return "ONLINE"
        return "PHYSICAL"


class BookingModeDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value == "BOOKING_ONLY":
            return "BOOK_ONLY"
        elif value == "BOOKING_AND_PAYMENT":
            return "BOOK_AND_PAY"
        return value

    def process_result_value(self, value, dialect):
        if value == "BOOK_ONLY":
            return "BOOKING_ONLY"
        elif value == "BOOK_AND_PAY":
            return "BOOKING_AND_PAYMENT"
        return value


class ServicePricing(Base):
    __tablename__ = "service_pricing"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serviceId = Column("service_id", UUID(as_uuid=True), ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    priceType = Column("price_type", String(50), default="FIXED", nullable=False)
    price = Column("price", Numeric(10, 2), nullable=False)
    currencyCode = Column("currency_code", String(3), default="INR", nullable=False)
    createdAt = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    service = relationship("Service", back_populates="pricing_rel")


class Service(Base):
    """
    SQLAlchemy model representing a Service entity.
    """
    __tablename__ = "services"
    __table_args__ = (
        {"extend_existing": True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    categoryId = Column("category_id", UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    serviceName = Column("service_name", String(150), nullable=False)
    serviceSlug = Column("service_slug", String(150), nullable=False)
    serviceType = Column("service_type_id", ServiceTypeInteger, default="PHYSICAL", nullable=False) # PHYSICAL or ONLINE
    description = Column("long_description", String(500), nullable=True) # maps to long_description
    duration = Column("duration_minutes", Integer, nullable=False) # Duration in minutes (maps to duration_minutes)
    
    primary_media_id = Column("primary_media_id", UUID(as_uuid=True), nullable=True)
    approvalStatus = Column("approval_status", String(50), default="PENDING", nullable=False) # PENDING, APPROVED, REJECTED
    status = Column("status", String(50), default="ACTIVE", nullable=False) # Maps to status (ACTIVE/INACTIVE)
    createdAt = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Missing database columns mapped with defaults to satisfy NOT NULL constraints
    storeId = Column("store_id", UUID(as_uuid=True), nullable=False, default=uuid.UUID("d7bb739c-d79d-4ffd-8426-c0378e423f87"))
    serviceCode = Column("service_code", String(100), nullable=False, default=lambda: str(uuid.uuid4())[:8])
    gstRate = Column("gst_rate", Numeric(10, 2), nullable=False, default=0.0)
    createdBy = Column("created_by", UUID(as_uuid=True), nullable=False, default=uuid.UUID("9c3e981e-1f81-4279-8d14-88481ff24588"))

    # Relationships
    category = relationship("Category")
    pricing_rel = relationship("ServicePricing", back_populates="service", cascade="all, delete-orphan", uselist=False, lazy="joined")
    bookingRules = relationship("BookingRule", back_populates="service", cascade="all, delete-orphan", lazy="selectin")
    availabilities = relationship("ServiceAvailability", back_populates="service", cascade="all, delete-orphan", lazy="selectin")

    def __init__(self, **kwargs):
        pricing_val = kwargs.pop("pricing", None)
        is_active_val = kwargs.pop("isActive", None)
        media_val = kwargs.pop("media", None)
        meta_title_val = kwargs.pop("metaTitle", None)
        meta_desc_val = kwargs.pop("metaDescription", None)
        meta_slug_val = kwargs.pop("metaSlug", None)
        super().__init__(**kwargs)
        if pricing_val is not None:
            self.pricing = pricing_val
        if is_active_val is not None:
            self.isActive = is_active_val
        if media_val is not None:
            self.media = media_val
        if meta_title_val is not None:
            self.metaTitle = meta_title_val
        if meta_desc_val is not None:
            self.metaDescription = meta_desc_val
        if meta_slug_val is not None:
            self.metaSlug = meta_slug_val

    # Hybrid property for pricing to delegate to ServicePricing relation
    @hybrid_property
    def pricing(self):
        return self.pricing_rel.price if self.pricing_rel else 0.0

    @pricing.setter
    def pricing(self, value):
        if not self.pricing_rel:
            self.pricing_rel = ServicePricing(price=value)
        else:
            self.pricing_rel.price = value

    @hybrid_property
    def isActive(self):
        return self.status == "ACTIVE"

    @isActive.setter
    def isActive(self, value):
        self.status = "ACTIVE" if value else "INACTIVE"

    @hybrid_property
    def media(self):
        return self.primary_media_id

    @media.setter
    def media(self, value):
        if isinstance(value, str):
            try:
                self.primary_media_id = uuid.UUID(value)
            except Exception:
                self.primary_media_id = None
        elif isinstance(value, uuid.UUID):
            self.primary_media_id = value
        else:
            self.primary_media_id = None

    @hybrid_property
    def metaTitle(self):
        return getattr(self, "_metaTitle", None)

    @metaTitle.setter
    def metaTitle(self, value):
        self._metaTitle = value

    @hybrid_property
    def metaDescription(self):
        return getattr(self, "_metaDescription", None)

    @metaDescription.setter
    def metaDescription(self, value):
        self._metaDescription = value

    @hybrid_property
    def metaSlug(self):
        return getattr(self, "_metaSlug", None)

    @metaSlug.setter
    def metaSlug(self, value):
        self._metaSlug = value


class BookingRule(Base):
    """
    SQLAlchemy model representing Booking Rules.
    """
    __tablename__ = "service_booking_settings"
    __table_args__ = (
        {"extend_existing": True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serviceId = Column("service_id", UUID(as_uuid=True), ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    bookingMode = Column("booking_mode", BookingModeDecorator, default="BOOKING_ONLY", nullable=False) # BOOKING_ONLY, BOOKING_AND_PAYMENT
    requiresApproval = Column("requires_approval", Boolean, default=False, nullable=False)
    createdAt = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships - Eager loaded using lazy="joined" to prevent greenlet async issues when reading parent properties
    service = relationship("Service", back_populates="bookingRules", lazy="joined")

    def __init__(self, **kwargs):
        tenant_id_val = kwargs.pop("tenantId", None)
        is_active_val = kwargs.pop("isActive", None)
        super().__init__(**kwargs)
        if tenant_id_val is not None:
            self.tenantId = tenant_id_val
        if is_active_val is not None:
            self.isActive = is_active_val

    @hybrid_property
    def tenantId(self):
        if "service" in self.__dict__ and self.service:
            return self.service.tenantId
        return getattr(self, "_tenantId", None)

    @tenantId.setter
    def tenantId(self, value):
        self._tenantId = value

    @hybrid_property
    def isActive(self):
        return True

    @isActive.setter
    def isActive(self, value):
        pass


class ServiceAvailability(Base):
    """
    SQLAlchemy model representing Service Availability timings.
    """
    __tablename__ = "service_availability"
    __table_args__ = (
        {"extend_existing": True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serviceId = Column("service_id", UUID(as_uuid=True), ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    dayOfWeek = Column("day_of_week", Integer, nullable=False) # 0-6 (Monday-Sunday)
    
    _startTime = Column("start_time", Time, nullable=False)
    _endTime = Column("end_time", Time, nullable=False)
    
    slotDurationMinutes = Column("slot_duration_minutes", Integer, nullable=False, default=60)
    isActive = Column("is_available", Boolean, default=True, nullable=False) # Maps to is_available column
    createdAt = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships - Eager loaded using lazy="joined" to prevent greenlet async issues when reading parent properties
    service = relationship("Service", back_populates="availabilities", lazy="joined")

    def __init__(self, **kwargs):
        tenant_id_val = kwargs.pop("tenantId", None)
        start_time_val = kwargs.pop("startTime", None)
        end_time_val = kwargs.pop("endTime", None)
        slot_duration_val = kwargs.pop("slotDurationMinutes", None)
        super().__init__(**kwargs)
        if tenant_id_val is not None:
            self.tenantId = tenant_id_val
        if start_time_val is not None:
            self.startTime = start_time_val
        if end_time_val is not None:
            self.endTime = end_time_val
        if slot_duration_val is not None:
            self.slotDurationMinutes = slot_duration_val

    @hybrid_property
    def tenantId(self):
        if "service" in self.__dict__ and self.service:
            return self.service.tenantId
        return getattr(self, "_tenantId", None)

    @tenantId.setter
    def tenantId(self, value):
        self._tenantId = value

    @hybrid_property
    def startTime(self):
        if isinstance(self._startTime, time):
            return self._startTime.strftime("%H:%M")
        return self._startTime

    @startTime.setter
    def startTime(self, value):
        if isinstance(value, str):
            self._startTime = datetime.strptime(value, "%H:%M").time()
        else:
            self._startTime = value

    @hybrid_property
    def endTime(self):
        if isinstance(self._endTime, time):
            return self._endTime.strftime("%H:%M")
        return self._endTime

    @endTime.setter
    def endTime(self, value):
        if isinstance(value, str):
            self._endTime = datetime.strptime(value, "%H:%M").time()
        else:
            self._endTime = value
