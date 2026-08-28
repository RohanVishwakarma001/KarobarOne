# ================================================================================
# FILE: schemas/github/wishlistSchema.py
# ================================================================================
# Author: Shlok Pallav
# Contact: shlokpallav@gmail.com
# Purpose:
#   Pydantic schemas for Wishlist APIs.
# ================================================================================

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class WishlistBase(BaseModel):
    customer_id: UUID
    store_id: UUID
    wishlist_name: str
    is_default: bool = False


class WishlistCreate(WishlistBase):
    pass


class WishlistUpdate(BaseModel):
    wishlist_name: str | None = None
    is_default: bool | None = None


class WishlistResponse(WishlistBase):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }