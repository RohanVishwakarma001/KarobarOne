# Owner: mousamdas156@gmail.com
import os
import tempfile
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from app.apps.invoiceGenerator.generateInvoice import generateInvoice

router = APIRouter(prefix="/invoice", tags=["Invoice Generator"])

import re
from pydantic import field_validator

GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")


class CompanySchema(BaseModel):
    gstin: str = "27AADCK1234A1Z5"
    name: str = "KAROBARONE PVT. LTD."
    address1: str = "Sector-5, Salt Lake, Kolkata - 700091"
    address2: str = "West Bengal, India"
    state: str = "West Bengal"
    contact: str = "+91-1234567890"

    @field_validator("gstin")
    @classmethod
    def validate_gstin(cls, v: str) -> str:
        if v and not GSTIN_REGEX.match(v.upper()):
            raise ValueError(f"Invalid GSTIN format: '{v}'")
        return v.upper()


class PartySchema(BaseModel):
    name: str
    address: str
    state: str = "West Bengal - 19"
    gstin: str = ""

    @field_validator("gstin")
    @classmethod
    def validate_gstin(cls, v: str) -> str:
        if v and not GSTIN_REGEX.match(v.upper()):
            raise ValueError(f"Invalid GSTIN format: '{v}'")
        return v.upper() if v else v


class InvoiceMetaSchema(BaseModel):
    number: str
    date: str
    payment_mode: str = "UPI"
    reverse_charge: str = "NO"
    buyer_order: str = ""
    supplier_ref: str = ""
    vehicle: str = ""
    delivery_date: str = ""
    transport: str = ""
    terms_of_delivery: str = ""


class InvoiceItemSchema(BaseModel):
    sr: int
    description: str
    hsn: str = "0000"
    qty: int
    unit: str = "Nos"
    rate: float
    gst_pct: int

    @field_validator("qty")
    @classmethod
    def validate_qty(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity must be greater than zero")
        return v


class BankSchema(BaseModel):
    name: str = "STATE BANK OF INDIA"
    branch: str = "Salt Lake, Kolkata"
    account: str = "XXXXXXXXXX"
    ifsc: str = "SBIN0XXXXXX"
    upi: str = "karobarone@sbi"


class InvoiceDataSchema(BaseModel):
    company: CompanySchema = CompanySchema()
    bill_to: PartySchema
    ship_to: PartySchema
    invoice: InvoiceMetaSchema
    items: List[InvoiceItemSchema]
    bank: BankSchema = BankSchema()
    declaration: List[str] = [
        "1. Subject to Kolkata jurisdiction",
        "2. Terms & conditions are subject to our trade policy",
        "3. Our risk & responsibility ceases after delivery of goods."
    ]

    @field_validator("items")
    @classmethod
    def validate_items(cls, v: List[InvoiceItemSchema]) -> List[InvoiceItemSchema]:
        if not v:
            raise ValueError("Invoice must contain at least one item")
        return v


@router.post("/generate")
def create_pdf_invoice(data: InvoiceDataSchema):
    invoice_dict = data.model_dump()
    
    logo_file = os.path.join(os.path.dirname(__file__), "../../apps/invoiceGenerator/company_logo.png")
    if os.path.exists(logo_file):
        invoice_dict["logo_path"] = logo_file
    else:
        invoice_dict["logo_path"] = None

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        generateInvoice(invoice_dict, tmp_path)
        with open(tmp_path, "rb") as f:
            pdf_bytes = f.read()
        return Response(content=pdf_bytes, media_type="application/pdf", headers={
            "Content-Disposition": f"attachment; filename=invoice_{data.invoice.number}.pdf"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate invoice: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

