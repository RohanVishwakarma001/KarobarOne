# Owner - pradhansaikat123@gmail.com
# Router for audit logs.
# Tracks modifications, operations, and logging on all system entities.

# Import typing decorators for response parsing
from typing import List, Optional
# Import UUID type for entity identifier tracking
from uuid import UUID
# Import endpoint handlers and status codes from FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
# Import database select helper class from SQLAlchemy
from sqlalchemy import select
# Import database session definition for transaction control
from sqlalchemy.ext.asyncio import AsyncSession
# Import RBAC dependencies
from app.core.rbac import Roles, require_role
# Import local session provider dependency
from app.db.session import getDb as get_db
# Import AuditLog database model definitions
from app.db.models.approvals import AuditLog
# Import Pydantic schemas for request validation
from app.schemas.approvals import AuditLogCreate, AuditLogResponse

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

@router.post(
    "/",
    response_model=AuditLogResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER))],
)
async def create_audit_log(payload: AuditLogCreate, db: AsyncSession = Depends(get_db)):
    data = payload.model_dump()
    if data.get("ipAddress") is not None:
        data["ipAddress"] = str(data["ipAddress"])
    dbLog = AuditLog(**data)
    db.add(dbLog)
    await db.commit()
    await db.refresh(dbLog)
    return dbLog


@router.get(
    "/",
    response_model=List[AuditLogResponse],
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.PLATFORM_STAFF))],
)
async def list_auditLogs(
    tenantId: Optional[UUID] = None,
    entityType: Optional[str] = None,
    entityId: Optional[UUID] = None,
    actionType: Optional[str] = None,
    performedBy: Optional[UUID] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    query = select(AuditLog)
    if tenantId:
        query = query.where(AuditLog.tenantId == tenantId)
    if entityType:
        query = query.where(AuditLog.entityType == entityType)
    if entityId:
        query = query.where(AuditLog.entityId == entityId)
    if actionType:
        query = query.where(AuditLog.actionType == actionType)
    if performedBy:
        query = query.where(AuditLog.performedBy == performedBy)

    query = query.order_by(AuditLog.createdAt.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get(
    "/{logId}",
    response_model=AuditLogResponse,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.PLATFORM_STAFF))],
)
async def get_audit_log(logId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AuditLog).where(AuditLog.id == logId)
    )
    dbLog = result.scalar_one_or_none()
    if not dbLog:
        raise HTTPException(status_code=404, detail="Audit log entry not found")
    return dbLog


