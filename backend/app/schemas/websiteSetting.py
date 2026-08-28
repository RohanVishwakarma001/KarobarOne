import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WebsiteSettingCreate(BaseModel):
    storeId: uuid.UUID
    siteTitle: str | None = Field(None, max_length=150)
    siteDescription: str | None = None
    faviconMediaId: uuid.UUID | None = None
    maintenanceMode: bool = False
    isPublic: bool = False


class WebsiteSettingUpdate(BaseModel):
    siteTitle: str | None = Field(None, max_length=150)
    siteDescription: str | None = None
    faviconMediaId: uuid.UUID | None = None
    maintenanceMode: bool | None = None
    isPublic: bool | None = None


class WebsiteSettingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    storeId: uuid.UUID
    siteTitle: str | None
    siteDescription: str | None
    faviconMediaId: uuid.UUID | None
    maintenanceMode: bool
    isPublic: bool
    createdAt: datetime
    updatedAt: datetime
