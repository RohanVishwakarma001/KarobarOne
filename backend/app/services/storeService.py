# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/storeService.py — Store Management Service
# ================================================================================
# Why this file is used:
#   - Manages storefront configurations and validates store slug parameters.
#
# What components are inside:
#   - StoreService:
#       - createStore()     -> Registers storefront configurations, checking slug uniqueness.
#       - getStore()        -> Resolves store identities.
#       - getStoreBySlug()  -> Finds storefronts matching URL slugs.
#       - listStores()      -> Returns active stores, optionally filtered by tenant.
#       - updateStore()     -> Modifies store configurations.
#       - deleteStore()     -> Removes store configurations, cascading relations.
# ================================================================================
"""
================================================================================
STORE SERVICE
================================================================================
Yeh file storefront objects ke business validation rules aur creation ko manage karti hai.
This service layer module implements core business logic for stores.

Why it is used:
- Validates the uniqueness of the store's web slug so routing URL works correctly.
- Prevents conflicts and coordinates transactions.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.store import Store
from app.repositories.storeRepository import StoreRepository
from app.schemas.store import StoreCreate, StoreUpdate


class StoreService:
    """
    Service class containing business rules for managing Store entities.
    """

    def __init__(self, session: AsyncSession):
        self.repo = StoreRepository(session)
        self.session = session

    async def createStore(self, data: StoreCreate) -> Store:
        """
        Creates a new storefront. Validates that the storeSlug is unique globally
        (otherwise routing URLs would conflict).
        """
        # Slug must be unique. (e.g. 'store-abc' shouldn't already be owned by someone else).
        if await self.repo.getBySlug(data.storeSlug):
            raise ConflictError(f"Store with slug '{data.storeSlug}' already exists")

        store = Store(**data.model_dump())
        result = await self.repo.create(store)
        await self.session.commit()
        return result

    async def getStore(self, storeId: uuid.UUID) -> Store:
        """
        Fetches a store by its unique database ID.
        """
        store = await self.repo.getById(storeId)
        if not store:
            raise NotFoundError("Store", str(storeId))
        return store

    async def getStoreBySlug(self, storeSlug: str) -> Store:
        """
        Fetches a store by its unique URL friendly slug.
        """
        store = await self.repo.getBySlug(storeSlug)
        if not store:
            raise NotFoundError("Store with slug", storeSlug)
        return store

    async def listStores(self, tenantId: uuid.UUID | None = None) -> Sequence[Store]:
        """
        Lists stores, optionally filtered to a specific tenant owner.
        """
        return await self.repo.getAll(tenantId=tenantId)

    async def updateStore(self, storeId: uuid.UUID, data: StoreUpdate) -> Store:
        """
        Updates an existing store's configuration. If the slug is changing,
        checks for slug uniqueness.
        """
        store = await self.repo.getById(storeId)
        if not store:
            raise NotFoundError("Store", str(storeId))

        updateData = data.model_dump(exclude_unset=True)
        # If modifying the URL slug, check if the new slug is already taken.
        if "storeSlug" in updateData:
            existing = await self.repo.getBySlug(updateData["storeSlug"])
            if existing and existing.id != storeId:
                raise ConflictError(f"Store with slug '{updateData['storeSlug']}' already exists")

        result = await self.repo.update(store, updateData)
        await self.session.commit()
        return result

    async def deleteStore(self, storeId: uuid.UUID) -> None:
        """
        Deletes a store and clears its cascade relations.
        """
        store = await self.repo.getById(storeId)
        if not store:
            raise NotFoundError("Store", str(storeId))
        await self.repo.delete(store)
        await self.session.commit()

        async def submitForApproval(self, storeId: uuid.UUID) -> Store:
         store = await self.repo.getById(storeId)

        if not store:
            raise NotFoundError("Store", str(storeId))

        if store.approvalStatus == "PENDING":
            raise ConflictError("Store is already pending approval")

        if store.approvalStatus == "APPROVED":
            raise ConflictError("Store is already approved")

        result = await self.repo.submitForApproval(store)
        await self.session.commit()
        return result


    async def publishStore(self, storeId: uuid.UUID) -> Store:
        store = await self.repo.getById(storeId)

        if not store:
            raise NotFoundError("Store", str(storeId))

        if store.approvalStatus != "APPROVED":
            raise ConflictError(
                "Store must be approved before publishing"
            )

        result = await self.repo.publish(store)
        await self.session.commit()
        return result

    async def previewStore(self, storeId: uuid.UUID) -> dict:
        """
        Returns preview information for a store website.
        """
        store = await self.repo.getById(storeId)

        if not store:
            raise NotFoundError("Store", str(storeId))

        return {
            "storeId": str(store.id),
            "storeName": store.storeName,
            "storeSlug": store.storeSlug,
            "approvalStatus": store.approvalStatus,
            "previewUrl": f"https://preview.karobarone.com/{store.storeSlug}",
        }

    async def changeTheme(
        self,
        storeId: uuid.UUID,
        themeId: uuid.UUID,
    ) -> Store:
        """
        Changes website theme.
        """
        store = await self.repo.getById(storeId)

        if not store:
            raise NotFoundError("Store", str(storeId))

        result = await self.repo.updateTheme(store, themeId)

        await self.session.commit()
        return result
    async def connectDomain(
        self,
        storeId: uuid.UUID,
        domain: str,
    ) -> dict:
        """
        Temporary custom domain API.
        """
        store = await self.repo.getById(storeId)

        if not store:
            raise NotFoundError("Store", str(storeId))

        return {
            "message": "Domain connected",
            "storeId": str(storeId),
            "domain": domain,
        }
    async def websiteStatus(
        self,
        storeId: uuid.UUID,
    ) -> dict:
        """
        Returns website status.
        """
        store = await self.repo.getById(storeId)

        if not store:
            raise NotFoundError("Store", str(storeId))

        return {
            "storeId": str(store.id),
            "status": store.approvalStatus,
            "isActive": store.isActive,
        }