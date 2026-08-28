# ================================================================================
# FILE: schemas/github/wishlistItemSchema.py
# ================================================================================
# Author: Shlok Pallav
# Contact: shlokpallav@gmail.com
# Purpose:
#   Pydantic schemas for Wishlist Item APIs.
# ================================================================================

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class WishlistItemBase(BaseModel):
    wishlist_id: UUID
    product_id: UUID
    product_variant_id: UUID | None = None


class WishlistItemCreate(WishlistItemBase):
    pass


class WishlistItemResponse(WishlistItemBase):
    id: UUID
    added_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }