# Owner - pradhansaikat123@gmail.com
# Customer router endpoints. Implements customer registration, paginated filtering,
# profiles, updates, and soft-delete features, secured with bcrypt hashing.
#
# This is the ACTIVE customer-management router (see docs/api-mapping/customers.md
# for the full ACTIVE/DEPRECATED/INTERNAL mapping across /customers,
# /customer-engine and /github/customers). Admin-facing endpoints below now
# require a staff bearer token (getCurrentUserId) and always scope by tenant
# (getTenantIdAsUUID) — previously tenant scoping could be bypassed entirely by
# passing a bare storeId, and there was no auth at all on customer PII reads.

import uuid
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, Query, status
from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import getSettings
from app.core.dependencies import getCurrentUserId
from app.core.exceptions import BadRequestError, ConflictError, NotFoundError
from app.core.tenantResolver import getTenantIdAsUUID
from app.db.session import getDb
from app.db.models.customers import Customer
from app.schemas.common import APIResponse
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


async def _getActiveCustomerOr404(db: AsyncSession, customerId: UUID) -> Customer:
    result = await db.execute(
        select(Customer).where(Customer.id == customerId, Customer.deletedAt.is_(None))
    )
    customer = result.scalar_one_or_none()
    if not customer:
        raise NotFoundError("Customer not found")
    return customer


# ── CREATE (public storefront registration — no staff bearer) ──
@router.post("/", response_model=APIResponse[CustomerResponse], status_code=status.HTTP_201_CREATED)
async def createCustomer(payload: CustomerCreate, db: AsyncSession = Depends(getDb)):
    existingEmail = await db.execute(
        select(Customer).where(
            Customer.storeId == payload.storeId,
            Customer.email == payload.email,
            Customer.deletedAt.is_(None),
        )
    )
    if existingEmail.scalar_one_or_none():
        raise ConflictError("Email already registered for this store")

    existingMobile = await db.execute(
        select(Customer).where(
            Customer.storeId == payload.storeId,
            Customer.mobile == payload.mobile,
            Customer.deletedAt.is_(None),
        )
    )
    if existingMobile.scalar_one_or_none():
        raise ConflictError("Mobile already registered for this store")

    data = payload.model_dump(exclude={"password"})
    if not data.get("customerCode"):
        data["customerCode"] = f"CUST-{uuid.uuid4().hex[:6].upper()}"
    if payload.password:
        data["passwordHash"] = pwd_context.hash(payload.password)

    customer = Customer(**data)
    db.add(customer)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        errMsg = str(e.orig) if hasattr(e, "orig") else str(e)
        if "fk_customer_tenant" in errMsg or "fk_customer_store" in errMsg or "tenants_details" in errMsg or "stores" in errMsg:
            logger.warning("DB FK failed for customer creation, using default fallback IDs", error=errMsg)
            customer.tenantId = UUID(settings.defaultTenantId)
            customer.storeId = UUID(settings.defaultStoreId)
            db.add(customer)
            try:
                await db.commit()
            except Exception as retryErr:
                await db.rollback()
                logger.error("Failed to commit customer even with fallback IDs", error=str(retryErr))
                raise BadRequestError("Could not create customer with provided tenant/store ID") from retryErr
        elif "uq_customers_store_email" in errMsg:
            raise ConflictError("Email already registered for this store") from e
        elif "uq_customers_store_mobile" in errMsg:
            raise ConflictError("Mobile already registered for this store") from e
        else:
            raise BadRequestError(f"Database integrity error: {errMsg}") from e

    await db.refresh(customer)
    return APIResponse(data=customer, message="Customer registered")


# ── LIST (paginated, staff-only, always tenant-scoped) ──
@router.get("/", response_model=APIResponse[PaginatedResponse])
async def listCustomers(
    storeId: Optional[UUID] = Query(None, description="Optional additional filter within the caller's tenant"),
    status_: Optional[str] = Query(None, alias="status"),
    isGuestCustomer: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    tenantId: UUID = Depends(getTenantIdAsUUID),
    _staffUserId: str = Depends(getCurrentUserId),
    db: AsyncSession = Depends(getDb),
):
    query = select(Customer).where(Customer.deletedAt.is_(None), Customer.tenantId == tenantId)
    if storeId:
        query = query.where(Customer.storeId == storeId)
    if status_:
        query = query.where(Customer.status == status_)
    if isGuestCustomer is not None:
        query = query.where(Customer.isGuestCustomer == isGuestCustomer)

    totalResult = await db.execute(select(func.count()).select_from(query.subquery()))
    total = totalResult.scalar()

    result = await db.execute(query.offset((page - 1) * pageSize).limit(pageSize))
    customers = result.scalars().all()

    return APIResponse(data={"total": total, "page": page, "pageSize": pageSize, "data": customers})


# ── GET BY ID (staff-only) ──
@router.get("/{customer_id}", response_model=APIResponse[CustomerResponse])
async def getCustomer(
    customer_id: UUID,
    tenantId: UUID = Depends(getTenantIdAsUUID),
    _staffUserId: str = Depends(getCurrentUserId),
    db: AsyncSession = Depends(getDb),
):
    customer = await _getActiveCustomerOr404(db, customer_id)
    if customer.tenantId != tenantId:
        raise NotFoundError("Customer not found")
    return APIResponse(data=customer)


# ── UPDATE (staff-only) ──
@router.patch("/{customer_id}", response_model=APIResponse[CustomerResponse])
async def updateCustomer(
    customer_id: UUID,
    payload: CustomerUpdate,
    tenantId: UUID = Depends(getTenantIdAsUUID),
    _staffUserId: str = Depends(getCurrentUserId),
    db: AsyncSession = Depends(getDb),
):
    customer = await _getActiveCustomerOr404(db, customer_id)
    if customer.tenantId != tenantId:
        raise NotFoundError("Customer not found")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(customer, field, value)

    await db.commit()
    await db.refresh(customer)
    return APIResponse(data=customer, message="Customer updated")


# ── SOFT DELETE (staff-only) ──
# 204 responses must carry no body per HTTP semantics, so this intentionally
# does NOT wrap in APIResponse — the envelope only applies where there's a body.
@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteCustomer(
    customer_id: UUID,
    tenantId: UUID = Depends(getTenantIdAsUUID),
    _staffUserId: str = Depends(getCurrentUserId),
    db: AsyncSession = Depends(getDb),
):
    customer = await _getActiveCustomerOr404(db, customer_id)
    if customer.tenantId != tenantId:
        raise NotFoundError("Customer not found")

    customer.deletedAt = datetime.now(timezone.utc)
    await db.commit()


# ── GET CUSTOMER WITH ADDRESSES (staff-only) ──
@router.get("/{customer_id}/full", response_model=APIResponse[CustomerResponse])
async def getCustomerFull(
    customer_id: UUID,
    tenantId: UUID = Depends(getTenantIdAsUUID),
    _staffUserId: str = Depends(getCurrentUserId),
    db: AsyncSession = Depends(getDb),
):
    """Returns customer with all addresses eagerly loaded (see Customer.addresses lazy='selectin')."""
    customer = await _getActiveCustomerOr404(db, customer_id)
    if customer.tenantId != tenantId:
        raise NotFoundError("Customer not found")
    return APIResponse(data=customer)


@router.get("/trash/list", response_model=APIResponse[PaginatedResponse])
async def listTrashCustomers(
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    tenantId: UUID = Depends(getTenantIdAsUUID),
    _staffUserId: str = Depends(getCurrentUserId),
    db: AsyncSession = Depends(getDb),
):
    query = select(Customer).where(Customer.deletedAt.is_not(None), Customer.tenantId == tenantId)
    totalResult = await db.execute(select(func.count()).select_from(query.subquery()))
    total = totalResult.scalar()

    result = await db.execute(query.offset((page - 1) * pageSize).limit(pageSize))
    customers = result.scalars().all()
    return APIResponse(data={"total": total, "page": page, "pageSize": pageSize, "data": customers})


@router.post("/{customer_id}/restore", response_model=APIResponse[CustomerResponse])
async def restoreCustomer(
    customer_id: UUID,
    tenantId: UUID = Depends(getTenantIdAsUUID),
    _staffUserId: str = Depends(getCurrentUserId),
    db: AsyncSession = Depends(getDb),
):
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id, Customer.deletedAt.is_not(None))
    )
    customer = result.scalar_one_or_none()
    if not customer or customer.tenantId != tenantId:
        raise NotFoundError("Deleted customer not found")

    customer.deletedAt = None
    await db.commit()
    await db.refresh(customer)
    return APIResponse(data=customer, message="Customer restored")
