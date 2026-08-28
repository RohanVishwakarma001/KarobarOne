import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WebsitePublishLogCreate(BaseModel):
    storeId: uuid.UUID
    deploymentId: uuid.UUID | None = None
    action: str = Field(..., max_length=30)
    status: str = Field(..., max_length=30)
    version: str | None = Field(None, max_length=100)
    message: str | None = None


class WebsitePublishLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    storeId: uuid.UUID
    deploymentId: uuid.UUID | None
    action: str
    status: str
    version: str | None
    message: str | None
    publishedAt: datetime | None
    createdAt: datetime
