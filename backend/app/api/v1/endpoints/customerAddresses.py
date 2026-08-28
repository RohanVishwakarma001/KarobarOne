# Owner - pradhansaikat123@gmail.com
# Customer addresses router. Manages customer shipping and billing addresses,
# ensuring the database correctly unsets previous defaults when a new default address is selected.

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb as get_db
from app.db.models.customers import CustomerAddress
from app.schemas.customers import (
    CustomerAddressCreate,
    CustomerAddressResponse,
    CustomerAddressUpdate,
)

router = APIRouter(prefix="/addresses", tags=["Customer Addresses"])


@router.post("/", response_model=CustomerAddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(payload: CustomerAddressCreate, db: AsyncSession = Depends(get_db)):
    # If this is set as default, unset other defaults for that customer & type
    if payload.isDefault:
        existing = await db.execute(
            select(CustomerAddress).where(
                CustomerAddress.customerId == payload.customerId,
                CustomerAddress.addressType == payload.addressType,
                CustomerAddress.isDefault == True,
            )
        )
        for addr in existing.scalars().all():
            addr.isDefault = False

    address = CustomerAddress(**payload.model_dump())
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address


@router.get("/customer/{customer_id}", response_model=List[CustomerAddressResponse])
async def list_addresses(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerAddress).where(CustomerAddress.customerId == customer_id)
    )
    return result.scalars().all()


@router.get("/{address_id}", response_model=CustomerAddressResponse)
async def get_address(address_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerAddress).where(CustomerAddress.id == address_id)
    )
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.patch("/{address_id}", response_model=CustomerAddressResponse)
async def update_address(
    address_id: UUID, payload: CustomerAddressUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(CustomerAddress).where(CustomerAddress.id == address_id)
    )
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    update_data = payload.model_dump(exclude_none=True)

    # Handle default flag update
    if update_data.get("isDefault"):
        existing = await db.execute(
            select(CustomerAddress).where(
                CustomerAddress.customerId == address.customerId,
                CustomerAddress.addressType == address.addressType,
                CustomerAddress.isDefault == True,
                CustomerAddress.id != address_id,
            )
        )
        for addr in existing.scalars().all():
            addr.isDefault = False

    for field, value in update_data.items():
        setattr(address, field, value)

    await db.commit()
    await db.refresh(address)
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerAddress).where(CustomerAddress.id == address_id)
    )
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    await db.delete(address)
    await db.commit()
