import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WebsiteAIContentCreate(BaseModel):
    storeId: uuid.UUID
    contentType: str = Field(..., max_length=50)
    content: str | None = None
    metadata: dict | list | None = None


class WebsiteAIContentUpdate(BaseModel):
    content: str | None = None
    metadata: dict | list | None = None
    status: str | None = Field(None, max_length=30)


class WebsiteAIContentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    storeId: uuid.UUID
    contentType: str
    content: str | None
    metadata: dict | list | None = Field(
        validation_alias="contentMetadata",
        serialization_alias="metadata",
    )
    status: str
    createdAt: datetime
    updatedAt: datetime
