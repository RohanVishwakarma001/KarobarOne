from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProductCompareListBase(BaseModel):
    customer_id: UUID
    store_id: UUID


class ProductCompareListCreate(ProductCompareListBase):
    pass


class ProductCompareListResponse(ProductCompareListBase):
    id: UUID
    created_at: datetime | None = None

    class Config:
        from_attributes = True