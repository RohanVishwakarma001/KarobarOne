# Owner - pradhansaikat123@gmail.com
# Customer sessions router. Tracks login state, user agent, IP address, and
# session expirations, with endpoints for listing, updating, and invalidation.

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb as get_db
from app.db.models.customers import CustomerSession
from app.schemas.customers import (
    CustomerSessionCreate,
    CustomerSessionResponse,
    CustomerSessionUpdate,
)

router = APIRouter(prefix="/sessions", tags=["Customer Sessions"])


@router.post("/", response_model=CustomerSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(payload: CustomerSessionCreate, db: AsyncSession = Depends(get_db)):
    session = CustomerSession(**payload.model_dump())
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


@router.get("/customer/{customer_id}", response_model=List[CustomerSessionResponse])
async def list_sessions(customer_id: UUID, active_only: bool = False, db: AsyncSession = Depends(get_db)):
    query = select(CustomerSession).where(CustomerSession.customerId == customer_id)
    if active_only:
        query = query.where(CustomerSession.isActive == True)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{session_id}", response_model=CustomerSessionResponse)
async def get_session(session_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CustomerSession).where(CustomerSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.patch("/{session_id}", response_model=CustomerSessionResponse)
async def update_session(
    session_id: UUID, payload: CustomerSessionUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(CustomerSession).where(CustomerSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(session, field, value)

    await db.commit()
    await db.refresh(session)
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def invalidate_session(session_id: UUID, db: AsyncSession = Depends(get_db)):
    """Hard delete a session record."""
    result = await db.execute(select(CustomerSession).where(CustomerSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    await db.delete(session)
    await db.commit()
