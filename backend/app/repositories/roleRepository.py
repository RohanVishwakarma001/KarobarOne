# Owner: mousamdas156@gmail.com
"""
Repository layer for Role.
Handles direct database queries for role definitions.
"""

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.role import Role


class RoleRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, roleId: uuid.UUID) -> Role | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(Role).where(Role.id == roleId)
        )
        return result.scalar_one_or_none()

    async def getByCode(self, roleCode: str) -> Role | None:
        """
        Handles the get by code functionality.
        """
        result = await self.session.execute(
            select(Role).where(Role.roleCode == roleCode)
        )
        return result.scalar_one_or_none()

    async def getAll(self) -> Sequence[Role]:
        """
        Handles the get all functionality.
        """
        result = await self.session.execute(
            select(Role).order_by(Role.createdAt.desc())
        )
        return result.scalars().all()

    async def create(self, role: Role) -> Role:
        """
        Handles the create functionality.
        """
        self.session.add(role)
        await self.session.flush()
        await self.session.refresh(role)
        return role

    async def update(self, role: Role, data: dict) -> Role:
        """
        Handles the update functionality.
        """
        for key, value in data.items():
            setattr(role, key, value)
        await self.session.flush()
        await self.session.refresh(role)
        return role

    async def delete(self, role: Role) -> None:
        """
        Handles the delete functionality.
        """
        await self.session.delete(role)
        await self.session.flush()
