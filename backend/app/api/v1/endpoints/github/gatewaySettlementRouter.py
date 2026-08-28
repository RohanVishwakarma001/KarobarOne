from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.gatewaySettlementController import (
    gatewaySettlementController,
)
from app.db.session import getSyncDb
from app.schemas.github.gatewaySettlementSchema import (
    GatewaySettlementCreate,
    GatewaySettlementUpdate,
)

router = APIRouter(
    prefix="/gateway-settlements",
    tags=["Gateway Settlements"]
)


@router.post("/")
def create(
    settlement: GatewaySettlementCreate,
    db: Session = Depends(getSyncDb)
):
    return gatewaySettlementController.create(
        db,
        settlement
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return gatewaySettlementController.getAll(db)


@router.get("/{settlementId}")
def getById(
    settlementId: UUID,
    db: Session = Depends(getSyncDb)
):
    return gatewaySettlementController.getById(
        db,
        settlementId
    )


@router.put("/{settlementId}")
def update(
    settlementId: UUID,
    settlement: GatewaySettlementUpdate,
    db: Session = Depends(getSyncDb)
):
    return gatewaySettlementController.update(
        db,
        settlementId,
        settlement
    )


@router.delete("/{settlementId}")
def delete(
    settlementId: UUID,
    db: Session = Depends(getSyncDb)
):
    return gatewaySettlementController.delete(
        db,
        settlementId
    )