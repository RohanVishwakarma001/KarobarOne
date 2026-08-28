import uuid

from pydantic import BaseModel, Field


class WebsiteMediaCreate(BaseModel):
    websiteId: uuid.UUID
    logo: str | None = None
    banner: str | None = None
    gallery: list[str] | None = None


class WebsiteMediaUpdate(BaseModel):
    logo: str | None = None
    banner: str | None = None
    gallery: list[str] | None = None


class WebsiteMediaResponse(BaseModel):
    id: uuid.UUID
    websiteId: uuid.UUID
    logo: str | None
    banner: str | None
    gallery: list | None

    model_config = {
        "from_attributes": True
    }
