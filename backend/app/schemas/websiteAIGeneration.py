import uuid

from pydantic import BaseModel, Field


class WebsiteAIGenerateRequest(BaseModel):
    storeId: uuid.UUID
    contentType: str = Field(
        ...,
        max_length=50,
    )
    instructions: str | None = Field(
        default=None,
        max_length=5000,
    )
