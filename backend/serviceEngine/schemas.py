# Owner-pradhansaikat123@gmail.com

from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from decimal import Decimal

class ServiceCategoryBase(BaseModel):
    tenantId: UUID = Field(..., description="The ID of the tenant owning the category")
    categoryName: str = Field(..., description="The name of the category")
    categorySlug: str = Field(..., description="The unique slug of the category")
    categoryType: Optional[str] = Field("SERVICE", description="Type of the category")

class ServiceCategoryCreate(ServiceCategoryBase):
    pass

class ServiceCategoryUpdate(BaseModel):
    categoryName: Optional[str] = Field(None, description="The name of the category")
    categorySlug: Optional[str] = Field(None, description="The unique slug of the category")
    categoryType: Optional[str] = Field(None, description="Type of the category")
    isActive: Optional[bool] = Field(None, description="Whether the category is active")

class ServiceCategoryResponse(ServiceCategoryBase):
    id: UUID
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}

class ServiceBase(BaseModel):
    tenantId: UUID = Field(..., description="The ID of the tenant owning the service")
    categoryId: UUID = Field(..., description="The ID of the category this service belongs to")
    serviceName: str = Field(..., description="The name of the service")
    serviceSlug: str = Field(..., description="The unique slug of the service")
    serviceType: str = Field(..., description="The type of service, e.g. PHYSICAL or ONLINE")
    description: Optional[str] = Field(None, description="Optional description of the service")
    pricing: Decimal = Field(..., description="Pricing of the service")
    duration: int = Field(..., description="Duration of the service in minutes")
    media: Optional[Any] = Field(None, description="JSON representing media attachments")
    metaTitle: Optional[str] = Field(None, description="SEO meta title")
    metaDescription: Optional[str] = Field(None, description="SEO meta description")
    metaSlug: Optional[str] = Field(None, description="SEO meta slug")
    approvalStatus: Optional[str] = Field("PENDING", description="Status of approval, e.g. PENDING, APPROVED, REJECTED")

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    categoryId: Optional[UUID] = Field(None)
    serviceName: Optional[str] = Field(None)
    serviceSlug: Optional[str] = Field(None)
    serviceType: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    pricing: Optional[Decimal] = Field(None)
    duration: Optional[int] = Field(None)
    media: Optional[Any] = Field(None)
    metaTitle: Optional[str] = Field(None)
    metaDescription: Optional[str] = Field(None)
    metaSlug: Optional[str] = Field(None)
    approvalStatus: Optional[str] = Field(None)
    isActive: Optional[bool] = Field(None)

class ServiceResponse(ServiceBase):
    id: UUID
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}

class BookingRuleBase(BaseModel):
    tenantId: UUID = Field(..., description="The ID of the tenant")
    serviceId: UUID = Field(..., description="The ID of the service")
    bookingMode: str = Field("BOOKING_ONLY", description="Booking mode, BOOKING_ONLY or BOOKING_AND_PAYMENT")
    requiresApproval: Optional[bool] = Field(False, description="Whether booking requires approval")

class BookingRuleCreate(BookingRuleBase):
    pass

class BookingRuleUpdate(BaseModel):
    bookingMode: Optional[str] = Field(None)
    requiresApproval: Optional[bool] = Field(None)
    isActive: Optional[bool] = Field(None)

class BookingRuleResponse(BookingRuleBase):
    id: UUID
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}

class ServiceAvailabilityBase(BaseModel):
    tenantId: UUID = Field(..., description="The ID of the tenant")
    serviceId: UUID = Field(..., description="The ID of the service")
    dayOfWeek: int = Field(..., ge=0, le=6, description="0 (Monday) to 6 (Sunday)")
    startTime: str = Field(..., description="Format HH:MM")
    endTime: str = Field(..., description="Format HH:MM")

class ServiceAvailabilityCreate(ServiceAvailabilityBase):
    pass

class ServiceAvailabilityUpdate(BaseModel):
    dayOfWeek: Optional[int] = Field(None, ge=0, le=6)
    startTime: Optional[str] = Field(None)
    endTime: Optional[str] = Field(None)
    isActive: Optional[bool] = Field(None)

class ServiceAvailabilityResponse(ServiceAvailabilityBase):
    id: UUID
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}

class BookingValidationRequest(BaseModel):
    tenantId: UUID = Field(..., description="ID of the service provider tenant")
    serviceId: UUID = Field(..., description="ID of the service being booked")
    isPaid: Optional[bool] = Field(False, description="Whether payment was processed for this booking")
    paymentReferenceId: Optional[str] = Field(None, description="Payment transaction reference ID if paid")
