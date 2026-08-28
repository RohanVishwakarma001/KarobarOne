# ================================================================================
# FILE: schemas/github/savedForLaterSchema.py
# ================================================================================
# Owner: Shlok Pallav
# Contact: shlokpallav@gmail.com
# Purpose:
#   Pydantic schemas for Saved For Later APIs.
# ================================================================================

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SavedForLaterBase(BaseModel):
    customer_id: UUID
    product_id: UUID
    product_variant_id: UUID | None = None
    quantity: int = 1


class SavedForLaterCreate(SavedForLaterBase):
    pass


class SavedForLaterUpdate(BaseModel):
    quantity: int | None = None


class SavedForLaterResponse(SavedForLaterBase):
    id: UUID
    added_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }