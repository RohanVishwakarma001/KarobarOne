from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.gatewaySettlementItemRepository import (
    gatewaySettlementItemRepository,
)
from app.schemas.github.gatewaySettlementItemSchema import (
    GatewaySettlementItemCreate,
    GatewaySettlementItemUpdate,
)


class GatewaySettlementItemService:

    def create(
        self,
        db: Session,
        item: GatewaySettlementItemCreate
    ):
        return gatewaySettlementItemRepository.create(
            db=db,
            obj=item
        )

    def getAll(
        self,
        db: Session
    ):
        return gatewaySettlementItemRepository.get_all(db)

    def getById(
        self,
        db: Session,
        itemId: UUID
    ):
        return gatewaySettlementItemRepository.get(
            db=db,
            obj_id=itemId,
            id_field=gatewaySettlementItemRepository.model.id
        )

    def update(
        self,
        db: Session,
        itemId: UUID,
        item: GatewaySettlementItemUpdate
    ):
        dbItem = self.getById(db, itemId)

        if dbItem is None:
            return None

        return gatewaySettlementItemRepository.update(
            db=db,
            db_obj=dbItem,
            obj=item
        )

    def delete(
        self,
        db: Session,
        itemId: UUID
    ):
        dbItem = self.getById(db, itemId)

        if dbItem is None:
            return False

        gatewaySettlementItemRepository.delete(
            db=db,
            db_obj=dbItem
        )

        return True


gatewaySettlementItemService = GatewaySettlementItemService()