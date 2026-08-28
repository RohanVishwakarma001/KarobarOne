# Owner: mousamdas156@gmail.com
"""
Repository for Tenant Settings operations.
Extends BaseRepository with query helper for settings.
"""
# Import uuid for lookup keys
import uuid
# Import select query builder from SQLAlchemy
from sqlalchemy import select
# Import database session control
from sqlalchemy.ext.asyncio import AsyncSession
# Import TenantSettings database model definition
from app.db.models.tenantSettings import TenantSettings
# Import Base generic repository
from app.repositories.base import BaseRepository


class TenantSettingsRepository(BaseRepository[TenantSettings]):
    """
    Repository class providing data access utilities for TenantSettings records.
    """
    def __init__(self, session: AsyncSession):
        # Initialize parent BaseRepository with TenantSettings target model class
        super().__init__(TenantSettings, session)

    async def getByTenantId(self, tenantId: uuid.UUID) -> TenantSettings | None:
        """
        Retrieves the TenantSettings record mapped to the given tenant ID.
        Returns None if settings are not yet initialized for the tenant.
        """
        result = await self.session.execute(
            select(TenantSettings).where(TenantSettings.tenantId == tenantId)
        )
        return result.scalar_one_or_none()
