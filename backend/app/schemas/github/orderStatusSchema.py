# Owner: shlokpallav@gmail.com

"""
===============================================================================
ORDER STATUS ENGINE SCHEMA
===============================================================================

Used for validating Order Status transitions.

===============================================================================
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrderStatusUpdateRequest(BaseModel):

    order_id: UUID = Field(
        ...,
        description="Order ID"
    )

    order_status: str = Field(
        ...,
        max_length=25,
        description="New Order Status"
    )

    payment_status: str | None = Field(
        default=None,
        max_length=25
    )

    fulfillment_status: str | None = Field(
        default=None,
        max_length=25
    )


class OrderStatusResponse(BaseModel):

    order_id: UUID

    order_status: str

    payment_status: str

    fulfillment_status: str

    message: str

    model_config = ConfigDict(
        from_attributes=True
    )