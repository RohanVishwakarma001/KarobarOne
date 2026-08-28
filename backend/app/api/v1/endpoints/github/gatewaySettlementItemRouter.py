from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.gatewaySettlementItemController import (
    gatewaySettlementItemController,
)
from app.db.session import getSyncDb
from app.schemas.github.gatewaySettlementItemSchema import (
    GatewaySettlementItemCreate,
    GatewaySettlementItemUpdate,
)

router = APIRouter(
    prefix="/gateway-settlement-items",
    tags=["Gateway Settlement Items"]
)


@router.post("/")
def create(
    item: GatewaySettlementItemCreate,
    db: Session = Depends(getSyncDb)
):
    return gatewaySettlementItemController.create(
        db,
        item
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return gatewaySettlementItemController.getAll(db)


@router.get("/{itemId}")
def getById(
    itemId: UUID,
    db: Session = Depends(getSyncDb)
):
    return gatewaySettlementItemController.getById(
        db,
        itemId
    )


@router.put("/{itemId}")
def update(
    itemId: UUID,
    item: GatewaySettlementItemUpdate,
    db: Session = Depends(getSyncDb)
):
    return gatewaySettlementItemController.update(
        db,
        itemId,
        item
    )


@router.delete("/{itemId}")
def delete(
    itemId: UUID,
    db: Session = Depends(getSyncDb)
):
    return gatewaySettlementItemController.delete(
        db,
        itemId
    )