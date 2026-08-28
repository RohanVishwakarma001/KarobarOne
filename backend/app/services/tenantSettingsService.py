# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/tenantSettingsService.py — Tenant Settings Service
# ================================================================================
# Why this file is used:
#   - Manages business logic and defaults generation for Tenant Settings.
#
# What components are inside:
#   - TenantSettingsService:
#       - getSettings()    -> Fetches or automatically seeds default settings.
#       - updateSettings() -> Performs partial updates to tenant settings configuration.
# ================================================================================
# Import uuid for entity lookup
import uuid
# Import session context control from SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
# Import custom NotFound exception
from app.core.exceptionsCompat import NotFoundError
# Import TenantSettings database model definition
from app.db.models.tenantSettings import TenantSettings
# Import repositories
from app.repositories.tenantSettingsRepository import TenantSettingsRepository
from app.repositories.tenantRepository import TenantRepository
# Import schemas for settings creation and update validations
from app.schemas.tenantSettings import TenantSettingsCreate, TenantSettingsUpdate


class TenantSettingsService:
    """
    Service class managing business logic for SaaS tenant profile settings.
    """
    def __init__(self, session: AsyncSession):
        # Initialize settings repository and tenant checks repository
        self.repo = TenantSettingsRepository(session)
        self.tenantRepo = TenantRepository(session)
        self.session = session

    async def getSettings(self, tenantId: uuid.UUID) -> TenantSettings:
        """
        Retrieves the settings configuration mapped to a specific tenant ID.
        If settings do not exist yet, initializes a default settings configuration in the database.
        """
        # Validate that the tenant exists and is active
        tenant = await self.tenantRepo.getById(tenantId)
        if not tenant:
            raise NotFoundError("Tenant", str(tenantId))
            
        # Attempt to retrieve current tenant settings
        settings = await self.repo.getByTenantId(tenantId)
        if not settings:
            # Lazy seeding: create default settings if none exist
            settings = TenantSettings(tenantId=tenantId)
            await self.repo.create(settings)
            await self.session.commit()
            
        return settings

    async def updateSettings(self, tenantId: uuid.UUID, data: TenantSettingsUpdate) -> TenantSettings:
        """
        Updates the settings profile configuration for the target tenant ID.
        Auto-generates the profile with default values if it is not yet initialized.
        """
        # Verify tenant existence
        tenant = await self.tenantRepo.getById(tenantId)
        if not tenant:
            raise NotFoundError("Tenant", str(tenantId))
            
        # Get active settings profile
        settings = await self.repo.getByTenantId(tenantId)
        if not settings:
            # If no settings profile exists yet, create one using update parameters
            create_data = data.model_dump(exclude_unset=True)
            settings = TenantSettings(tenantId=tenantId, **create_data)
            await self.repo.create(settings)
        else:
            # Perform partial update with provided parameters
            updateData = data.model_dump(exclude_unset=True)
            if updateData:
                await self.repo.update(settings, updateData)
                
        await self.session.commit()
        return await self.repo.getByTenantId(tenantId)
