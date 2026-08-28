import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict


class WebsitePreviewSection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sectionName: str
    content: dict | list | None


class WebsitePreviewMedia(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    logo: str | None
    banner: str | None
    gallery: list | None


class WebsitePreviewTheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    themeName: str
    themeCode: str
    configSchema: dict | list | None
    isActive: bool


class WebsitePreviewResponse(BaseModel):
    website: dict[str, Any]
    sections: list[WebsitePreviewSection]
    media: WebsitePreviewMedia | None
    theme: WebsitePreviewTheme | None
    preview: bool = True
