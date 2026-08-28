# Owner - pradhansaikat123@gmail.com
# Router for status history tracking.
# Tracks status transitions across various system entities like PRODUCTS, ORDERS, BOOKINGS, etc.

# Import typing decorators for lists and optionals
from typing import List, Optional
# Import UUID class for typing unique entity identifiers
from uuid import UUID
# Import FastAPI handlers, dependency injection and statuses
from fastapi import APIRouter, Depends, HTTPException, status
# Import select query builder from SQLAlchemy
from sqlalchemy import select
# Import transaction session for database execution control
from sqlalchemy.ext.asyncio import AsyncSession
# Import database session getter utility
from app.db.session import getDb as get_db
# Import StatusHistory database model definition
from app.db.models.approvals import StatusHistory
# Import schemas for status validation and response styling
from app.schemas.approvals import StatusHistoryCreate, StatusHistoryResponse

router = APIRouter(prefix="/status-history", tags=["Status History"])

@router.post("/", response_model=StatusHistoryResponse, status_code=status.HTTP_201_CREATED)
async def create_statusHistory(payload: StatusHistoryCreate, db: AsyncSession = Depends(get_db)):
    dbHistory = StatusHistory(**payload.model_dump())
    db.add(dbHistory)
    await db.commit()
    await db.refresh(dbHistory)
    return dbHistory


@router.get("/", response_model=List[StatusHistoryResponse])
async def list_statusHistory(
    tenantId: Optional[UUID] = None,
    entityType: Optional[str] = None,
    entityId: Optional[UUID] = None,
    newStatus: Optional[str] = None,
    changedBy: Optional[UUID] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    query = select(StatusHistory)
    if tenantId:
        query = query.where(StatusHistory.tenantId == tenantId)
    if entityType:
        query = query.where(StatusHistory.entityType == entityType)
    if entityId:
        query = query.where(StatusHistory.entityId == entityId)
    if newStatus:
        query = query.where(StatusHistory.newStatus == newStatus)
    if changedBy:
        query = query.where(StatusHistory.changedBy == changedBy)

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{historyId}", response_model=StatusHistoryResponse)
async def get_statusHistory(historyId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StatusHistory).where(StatusHistory.id == historyId)
    )
    dbHistory = result.scalar_one_or_none()
    if not dbHistory:
        raise HTTPException(status_code=404, detail="Status history record not found")
    return dbHistory


@router.delete("/{historyId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_statusHistory(historyId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StatusHistory).where(StatusHistory.id == historyId)
    )
    dbHistory = result.scalar_one_or_none()
    if not dbHistory:
        raise HTTPException(status_code=404, detail="Status history record not found")

    await db.delete(dbHistory)
    await db.commit()
