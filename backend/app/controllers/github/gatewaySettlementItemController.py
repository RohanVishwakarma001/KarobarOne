from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.gatewaySettlementItemSchema import (
    GatewaySettlementItemCreate,
    GatewaySettlementItemUpdate,
)
from app.services.github.gatewaySettlementItemService import (
    gatewaySettlementItemService,
)


class GatewaySettlementItemController:

    def create(
        self,
        db: Session,
        item: GatewaySettlementItemCreate
    ):
        return gatewaySettlementItemService.create(
            db,
            item
        )

    def getAll(
        self,
        db: Session
    ):
        return gatewaySettlementItemService.getAll(db)

    def getById(
        self,
        db: Session,
        itemId: UUID
    ):
        item = gatewaySettlementItemService.getById(
            db,
            itemId
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Settlement item not found."
            )

        return item

    def update(
        self,
        db: Session,
        itemId: UUID,
        item: GatewaySettlementItemUpdate
    ):
        dbItem = gatewaySettlementItemService.update(
            db,
            itemId,
            item
        )

        if dbItem is None:
            raise HTTPException(
                status_code=404,
                detail="Settlement item not found."
            )

        return dbItem

    def delete(
        self,
        db: Session,
        itemId: UUID
    ):
        deleted = gatewaySettlementItemService.delete(
            db,
            itemId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Settlement item not found."
            )

        return {
            "message": "Settlement item deleted successfully."
        }


gatewaySettlementItemController = GatewaySettlementItemController()