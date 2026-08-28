# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/statusService.py — Tenant Status Lookup Service
# ================================================================================
# Why this file is used:
#   - Manages status values (ACTIVE, SUSPENDED) in the master lookup tables.
#
# What components are inside:
#   - StatusService:
#       - listStatuses()   -> Returns status profiles.
#       - createStatus()   -> Registers new statuses, checking code uniqueness.
# ================================================================================
"""
Service layer for TenantStatus.
Handles fetching and registering tenant statuses.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.tenantStatus import TenantStatus
from app.repositories.statusRepository import StatusRepository
from app.schemas.status import StatusCreate


class StatusService:
    """
    Manages tenant subscription status definitions (e.g. ACTIVE, SUSPENDED).
    """
    def __init__(self, session: AsyncSession):
        self.repo = StatusRepository(session)
        self.session = session

    async def listStatuses(self) -> list[TenantStatus]:
        """
        Lists all status definitions available in the system.
        """
        return await self.repo.getAll()

    async def createStatus(self, data: StatusCreate) -> TenantStatus:
        """
        Registers a new status code definition in the status lookup table.
        """
        # Ensure status name is unique
        existing = await self.repo.getByName(data.statusName)
        if existing:
            raise ConflictError(
                f"Status '{data.statusName}' already exists"
            )
        status = TenantStatus(
            statusName=data.statusName,
            statusDescription=data.statusDescription,
        )
        result = await self.repo.create(status)
        await self.session.commit()
        return result