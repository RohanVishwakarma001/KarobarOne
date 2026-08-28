import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WebsiteCreate(BaseModel):
    tenantId: uuid.UUID
    companyName: str = Field(..., min_length=1, max_length=255)
    businessType: str = Field(..., min_length=1, max_length=100)
    theme: str | None = Field(None, max_length=100)
    plan: str = Field("FREE", max_length=30)
    domain: str | None = Field(None, max_length=255)


class WebsiteUpdate(BaseModel):
    companyName: str | None = Field(None, min_length=1, max_length=255)
    businessType: str | None = Field(None, min_length=1, max_length=100)
    theme: str | None = Field(None, max_length=100)
    plan: str | None = Field(None, max_length=30)
    domain: str | None = Field(None, max_length=255)


class WebsiteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenantId: uuid.UUID
    companyName: str
    slug: str
    businessType: str
    theme: str | None
    status: str
    plan: str
    domain: str | None
    createdAt: datetime


class WebsiteSubmitRequest(BaseModel):
    websiteId: uuid.UUID


class WebsiteStatusRequest(BaseModel):
    websiteId: uuid.UUID
    reason: str | None = None
