# Owner - pradhansaikat123@gmail.com

# Application configuration using Pydantic Settings.
# Manages database credentials, image constraints, and JWT settings.

# Import Pydantic Settings to manage application configuration settings
from pydantic_settings import BaseSettings
# Import List from typing for type annotations
from typing import List
# Import Field from pydantic to define settings metadata and validation aliases
from pydantic import Field

class Settings(BaseSettings):
    databaseUrl: str = Field(
        ...,
        validation_alias="DATABASE_URL",
    )
    secretKey: str = Field(..., validation_alias="SECRET_KEY")
    algorithm: str = Field("HS256", validation_alias="ALGORITHM")
    accessTokenExpireMinutes: int = Field(30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    dropboxAccessToken: str = Field(..., validation_alias="DROPBOX_ACCESS_TOKEN")

    # Image upload validations
    maxImagesPerProduct: int = Field(5, validation_alias="MAX_IMAGES_PER_PRODUCT")
    maxImageSizeBytes: int = Field(5242880, validation_alias="MAX_IMAGE_SIZE_BYTES")
    allowedImageTypes: List[str] = Field(
        ["image/jpeg", "image/jpg", "image/png", "image/webp"],
        validation_alias="ALLOWED_IMAGE_TYPES"
    )

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
