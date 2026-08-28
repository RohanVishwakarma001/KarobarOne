import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WebsiteDeploymentCreate(BaseModel):
    storeId: uuid.UUID
    deploymentId: str | None = Field(None, max_length=255)
    provider: str = Field(..., max_length=50)


class WebsiteDeploymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    storeId: uuid.UUID
    deploymentId: str | None
    provider: str
    status: str
    deploymentUrl: str | None
    errorMessage: str | None
    startedAt: datetime | None
    completedAt: datetime | None
    createdAt: datetime
