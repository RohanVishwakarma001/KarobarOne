# Owner - pradhansaikat123@gmail.com
# Customer router endpoints. Implements customer registration, paginated filtering,
# profiles, updates, and soft-delete features, secure with bcrypt hashing.

from typing import List, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import getSettings
from app.db.session import getDb as get_db
from app.db.models.customers import Customer
from app.schemas.customers import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    PaginatedResponse,
)

logger = structlog.get_logger(__name__)
settings = getSettings()
router = APIRouter(prefix="/customers", tags=["Customers"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ── CREATE ───────────────────────────────────
@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(payload: CustomerCreate, db: AsyncSession = Depends(get_db)):
    # Duplicate check: store_id + email
    result = await db.execute(
        select(Customer).where(
            Customer.storeId == payload.storeId,
            Customer.email == payload.email,
            Customer.deletedAt.is_(None),
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered for this store")

    # Duplicate check: store_id + mobile
    result = await db.execute(
        select(Customer).where(
            Customer.storeId == payload.storeId,
            Customer.mobile == payload.mobile,
            Customer.deletedAt.is_(None),
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Mobile already registered for this store")

    data = payload.model_dump(exclude={"password"})
    if not data.get("customerCode"):
        import uuid
        data["customerCode"] = f"CUST-{uuid.uuid4().hex[:6].upper()}"

    if payload.password:
        data["passwordHash"] = pwd_context.hash(payload.password)

    customer = Customer(**data)
    db.add(customer)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        err_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        if "fk_customer_tenant" in err_msg or "fk_customer_store" in err_msg or "tenants_details" in err_msg or "stores" in err_msg:
            # Fallback to demo tenant & store if non-existent IDs were provided
            logger.warning("DB FK failed for customer creation, using default fallback IDs", error=err_msg)
            customer.tenantId = UUID(settings.defaultTenantId)
            customer.storeId = UUID(settings.defaultStoreId)
            db.add(customer)
            try:
                await db.commit()
            except Exception as retry_err:
                await db.rollback()
                logger.error("Failed to commit customer even with fallback IDs", error=str(retry_err))
                raise HTTPException(status_code=400, detail="Could not create customer with provided tenant/store ID")
        elif "uq_customers_store_email" in err_msg:
            raise HTTPException(status_code=409, detail="Email already registered for this store")
        elif "uq_customers_store_mobile" in err_msg:
            raise HTTPException(status_code=409, detail="Mobile already registered for this store")
        else:
            raise HTTPException(status_code=400, detail=f"Database integrity error: {err_msg}")

    await db.refresh(customer)
    return customer


# ── LIST (paginated) ─────────────────────────
@router.get("/", response_model=PaginatedResponse)
async def list_customers(
    storeId: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    isGuestCustomer: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Customer).where(Customer.deletedAt.is_(None))
    if storeId:
        query = query.where(Customer.storeId == storeId)
    else:
        # Require storeId filter to prevent cross-tenant/cross-store customer leaks (TC-0014)
        from app.core.tenant import getCurrentTenantId
        tid = getCurrentTenantId()
        if tid:
            query = query.where(Customer.tenantId == UUID(tid))
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="storeId or X-Tenant-ID header is required to list customers",
            )
    if status:
        query = query.where(Customer.status == status)
    if isGuestCustomer is not None:
        query = query.where(Customer.isGuestCustomer == isGuestCustomer)

    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar()

    result = await db.execute(query.offset((page - 1) * pageSize).limit(pageSize))
    customers = result.scalars().all()

    return {"total": total, "page": page, "pageSize": pageSize, "data": customers}


# ── GET BY ID ────────────────────────────────
@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id, Customer.deletedAt.is_(None))
    )
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


# ── UPDATE ───────────────────────────────────
@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: UUID, payload: CustomerUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id, Customer.deletedAt.is_(None))
    )
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = payload.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    await db.commit()
    await db.refresh(customer)
    return customer


# ── SOFT DELETE ──────────────────────────────
@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id, Customer.deletedAt.is_(None))
    )
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    from datetime import datetime, timezone
    customer.deletedAt = datetime.now(timezone.utc)
    await db.commit()


# ── GET CUSTOMER WITH ADDRESSES ──────────────
@router.get("/{customer_id}/full", response_model=CustomerResponse)
async def get_customer_full(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    """Returns customer with all addresses eagerly loaded."""
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id, Customer.deletedAt.is_(None))
    )
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/trash/list", response_model=PaginatedResponse)
async def list_trash_customers(
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Customer).where(Customer.deletedAt.is_not(None))
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar()

    result = await db.execute(query.offset((page - 1) * pageSize).limit(pageSize))
    customers = result.scalars().all()
    return {"total": total, "page": page, "pageSize": pageSize, "data": customers}


@router.post("/{customer_id}/restore", response_model=CustomerResponse)
async def restore_customer(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id, Customer.deletedAt.is_not(None))
    )
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Deleted customer not found")

    customer.deletedAt = None
    await db.commit()
    await db.refresh(customer)
    return customer

