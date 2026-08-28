# ================================================================================
# FILE: schemas/github/recentlyViewedProductSchema.py
# ================================================================================
# Owner: shlokpallav@gmail.com
# ================================================================================
# Purpose:
#     Pydantic schemas for Recently Viewed Product APIs.
# ================================================================================

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RecentlyViewedProductBase(BaseModel):
    customer_id: UUID
    product_id: UUID


class RecentlyViewedProductCreate(RecentlyViewedProductBase):
    pass


class RecentlyViewedProductResponse(RecentlyViewedProductBase):
    id: UUID
    viewed_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }