# Owner - pradhansaikat123@gmail.com
# Router endpoints for customer activities, note logs, user segments/groups,
# legal consent history, and password reset security token lifecycles.
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb as get_db
from app.db.models.customers import (
    CustomerActivityLog,
    CustomerConsentLog,
    CustomerGroup,
    CustomerGroupMember,
    CustomerNote,
    CustomerPasswordResetToken,
)
from app.schemas.customers import (
    CustomerActivityLogCreate,
    CustomerActivityLogResponse,
    CustomerConsentLogCreate,
    CustomerConsentLogResponse,
    CustomerGroupCreate,
    CustomerGroupMemberCreate,
    CustomerGroupMemberResponse,
    CustomerGroupResponse,
    CustomerGroupUpdate,
    CustomerNoteCreate,
    CustomerNoteResponse,
    CustomerNoteUpdate,
    PasswordResetTokenCreate,
    PasswordResetTokenResponse,
)

# ═══════════════════════════════════════════════
# ACTIVITY LOGS
# ═══════════════════════════════════════════════
activity_router = APIRouter(prefix="/activity-logs", tags=["Activity Logs"])


@activity_router.post("/", response_model=CustomerActivityLogResponse, status_code=201)
async def log_activity(payload: CustomerActivityLogCreate, db: AsyncSession = Depends(get_db)):
    log = CustomerActivityLog(**payload.model_dump())
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@activity_router.get("/customer/{customer_id}", response_model=List[CustomerActivityLogResponse])
async def list_customer_activities(
    customer_id: UUID,
    activityType: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(CustomerActivityLog).where(CustomerActivityLog.customerId == customer_id)
    if activityType:
        query = query.where(CustomerActivityLog.activityType == activityType)
    query = query.order_by(CustomerActivityLog.createdAt.desc())
    query = query.offset((page - 1) * pageSize).limit(pageSize)
    result = await db.execute(query)
    return result.scalars().all()


@activity_router.get("/{log_id}", response_model=CustomerActivityLogResponse)
async def get_activity_log(log_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CustomerActivityLog).where(CustomerActivityLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return log


# ═══════════════════════════════════════════════
# CUSTOMER GROUPS
# ═══════════════════════════════════════════════
groups_router = APIRouter(prefix="/groups", tags=["Customer Groups"])


@groups_router.post("/", response_model=CustomerGroupResponse, status_code=201)
async def create_group(payload: CustomerGroupCreate, db: AsyncSession = Depends(get_db)):
    group = CustomerGroup(**payload.model_dump())
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group


@groups_router.get("/", response_model=List[CustomerGroupResponse])
async def list_groups(storeId: Optional[UUID] = Query(None), db: AsyncSession = Depends(get_db)):
    query = select(CustomerGroup)
    if storeId:
        query = query.where(CustomerGroup.storeId == storeId)
    result = await db.execute(query)
    return result.scalars().all()


@groups_router.get("/{group_id}", response_model=CustomerGroupResponse)
async def get_group(group_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CustomerGroup).where(CustomerGroup.id == group_id))
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@groups_router.patch("/{group_id}", response_model=CustomerGroupResponse)
async def update_group(
    group_id: UUID, payload: CustomerGroupUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(CustomerGroup).where(CustomerGroup.id == group_id))
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(group, field, value)
    await db.commit()
    await db.refresh(group)
    return group


@groups_router.delete("/{group_id}", status_code=204)
async def delete_group(group_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CustomerGroup).where(CustomerGroup.id == group_id))
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    await db.delete(group)
    await db.commit()


# ── GROUP MEMBERS ────────────────────────────
@groups_router.post("/{group_id}/members", response_model=CustomerGroupMemberResponse, status_code=201)
async def add_member(
    group_id: UUID, payload: CustomerGroupMemberCreate, db: AsyncSession = Depends(get_db)
):
    payload_data = payload.model_dump()
    payload_data["groupId"] = group_id  # enforce URL param

    existing = await db.execute(
        select(CustomerGroupMember).where(
            CustomerGroupMember.customerId == payload.customerId,
            CustomerGroupMember.groupId == group_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Customer is already a member of this group")

    member = CustomerGroupMember(**payload_data)
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member


@groups_router.get("/{group_id}/members", response_model=List[CustomerGroupMemberResponse])
async def list_members(group_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerGroupMember).where(CustomerGroupMember.groupId == group_id)
    )
    return result.scalars().all()


@groups_router.delete("/{group_id}/members/{customer_id}", status_code=204)
async def remove_member(group_id: UUID, customer_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerGroupMember).where(
            CustomerGroupMember.groupId == group_id,
            CustomerGroupMember.customerId == customer_id,
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Membership not found")
    await db.delete(member)
    await db.commit()


# ═══════════════════════════════════════════════
# CUSTOMER NOTES
# ═══════════════════════════════════════════════
notes_router = APIRouter(prefix="/notes", tags=["Customer Notes"])


@notes_router.post("/", response_model=CustomerNoteResponse, status_code=201)
async def create_note(payload: CustomerNoteCreate, db: AsyncSession = Depends(get_db)):
    note = CustomerNote(**payload.model_dump())
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


@notes_router.get("/customer/{customer_id}", response_model=List[CustomerNoteResponse])
async def list_notes(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerNote).where(CustomerNote.customerId == customer_id)
        .order_by(CustomerNote.createdAt.desc())
    )
    return result.scalars().all()


@notes_router.get("/{note_id}", response_model=CustomerNoteResponse)
async def get_note(note_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CustomerNote).where(CustomerNote.id == note_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@notes_router.patch("/{note_id}", response_model=CustomerNoteResponse)
async def update_note(
    note_id: UUID, payload: CustomerNoteUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(CustomerNote).where(CustomerNote.id == note_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.noteText = payload.noteText
    await db.commit()
    await db.refresh(note)
    return note


@notes_router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CustomerNote).where(CustomerNote.id == note_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await db.delete(note)
    await db.commit()


# ═══════════════════════════════════════════════
# CONSENT LOGS
# ═══════════════════════════════════════════════
consent_router = APIRouter(prefix="/consents", tags=["Customer Consents"])


@consent_router.post("/", response_model=CustomerConsentLogResponse, status_code=201)
async def log_consent(payload: CustomerConsentLogCreate, db: AsyncSession = Depends(get_db)):
    consent = CustomerConsentLog(**payload.model_dump())
    db.add(consent)
    await db.commit()
    await db.refresh(consent)
    return consent


@consent_router.get("/customer/{customer_id}", response_model=List[CustomerConsentLogResponse])
async def list_consents(
    customer_id: UUID,
    consentType: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(CustomerConsentLog).where(CustomerConsentLog.customerId == customer_id)
    if consentType:
        query = query.where(CustomerConsentLog.consentType == consentType)
    result = await db.execute(query.order_by(CustomerConsentLog.acceptedAt.desc()))
    return result.scalars().all()


@consent_router.get("/{consent_id}", response_model=CustomerConsentLogResponse)
async def get_consent(consent_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CustomerConsentLog).where(CustomerConsentLog.id == consent_id))
    consent = result.scalar_one_or_none()
    if not consent:
        raise HTTPException(status_code=404, detail="Consent record not found")
    return consent


# ═══════════════════════════════════════════════
# PASSWORD RESET TOKENS
# ═══════════════════════════════════════════════
password_reset_router = APIRouter(prefix="/password-reset-tokens", tags=["Password Reset"])


@password_reset_router.post("/", response_model=PasswordResetTokenResponse, status_code=201)
async def create_token(payload: PasswordResetTokenCreate, db: AsyncSession = Depends(get_db)):
    token = CustomerPasswordResetToken(**payload.model_dump())
    db.add(token)
    await db.commit()
    await db.refresh(token)
    return token


@password_reset_router.get("/customer/{customer_id}", response_model=List[PasswordResetTokenResponse])
async def list_tokens(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerPasswordResetToken)
        .where(CustomerPasswordResetToken.customerId == customer_id)
        .order_by(CustomerPasswordResetToken.createdAt.desc())
    )
    return result.scalars().all()


@password_reset_router.patch("/{token_id}/mark-used", response_model=PasswordResetTokenResponse)
async def mark_token_used(token_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerPasswordResetToken).where(CustomerPasswordResetToken.id == token_id)
    )
    token = result.scalar_one_or_none()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    if token.usedAt:
        raise HTTPException(status_code=409, detail="Token already used")
    token.usedAt = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(token)
    return token


@password_reset_router.delete("/{token_id}", status_code=204)
async def delete_token(token_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerPasswordResetToken).where(CustomerPasswordResetToken.id == token_id)
    )
    token = result.scalar_one_or_none()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    await db.delete(token)
    await db.commit()
