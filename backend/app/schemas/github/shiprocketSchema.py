from typing import List, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)


class ShiprocketLoginRequest(BaseModel):

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6
    )


class OrderItem(BaseModel):

    name: str

    sku: str

    units: int = Field(
        ...,
        gt=0
    )

    selling_price: float = Field(
        ...,
        gt=0
    )


class CreateOrderRequest(BaseModel):

    order_id: str

    order_date: str

    pickup_location: str

    billing_customer_name: str

    billing_last_name: Optional[str] = ""

    billing_address: str

    billing_address_2: Optional[str] = ""

    billing_city: str

    billing_pincode: str

    billing_state: str

    billing_country: str

    billing_email: EmailStr

    billing_phone: str

    shipping_is_billing: bool = True

    shipping_customer_name: Optional[str] = None

    shipping_last_name: Optional[str] = None

    shipping_address: Optional[str] = None

    shipping_address_2: Optional[str] = None

    shipping_city: Optional[str] = None

    shipping_pincode: Optional[str] = None

    shipping_state: Optional[str] = None

    shipping_country: Optional[str] = None

    shipping_phone: Optional[str] = None

    order_items: List[OrderItem]

    payment_method: str

    sub_total: float = Field(
        ...,
        gt=0
    )

    length: float = Field(
        ...,
        gt=0
    )

    breadth: float = Field(
        ...,
        gt=0
    )

    height: float = Field(
        ...,
        gt=0
    )

    weight: float = Field(
        ...,
        gt=0
    )

    channel_id: Optional[str] = ""


class ServiceabilityRequest(BaseModel):

    pickup_postcode: str

    delivery_postcode: str

    weight: float = Field(
        ...,
        gt=0
    )

    cod: int = 0


class CourierRecommendationRequest(BaseModel):

    pickup_postcode: str

    delivery_postcode: str

    weight: float = Field(
        ...,
        gt=0
    )

    cod: int = 0


class GenerateAwbRequest(BaseModel):

    shipment_id: int

    courier_id: int


class PickupRequest(BaseModel):

    shipment_id: List[int]


class LabelRequest(BaseModel):

    shipment_id: List[int]


class InvoiceRequest(BaseModel):

    shipment_id: List[int]


class ManifestRequest(BaseModel):

    shipment_id: List[int]
    
class UpdateOrderRequest(BaseModel):

    order_id: int

    order_status: str


class ShiprocketOrderResponse(BaseModel):

    success: bool

    data: dict
    
class PickupLocationRequest(BaseModel):

    pickup_location: str
    name: str
    email: EmailStr
    phone: str
    address: str
    address_2: str = ""
    city: str
    state: str
    country: str = "India"
    pin_code: str


class PickupLocationResponse(BaseModel):

    success: bool
    message: str
class NdrActionRequest(BaseModel):

    shipment_id: int
    action: str
    comments: str = ""