from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.sellerPayoutController import (
    sellerPayoutController,
)
from app.db.session import getSyncDb
from app.schemas.github.sellerPayoutSchema import (
    SellerPayoutCreate,
    SellerPayoutUpdate,
)

router = APIRouter(
    prefix="/seller-payouts",
    tags=["Seller Payouts"]
)


@router.post("/")
def create(
    payout: SellerPayoutCreate,
    db: Session = Depends(getSyncDb)
):
    return sellerPayoutController.create(
        db,
        payout
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return sellerPayoutController.getAll(db)


@router.get("/{payoutId}")
def getById(
    payoutId: UUID,
    db: Session = Depends(getSyncDb)
):
    return sellerPayoutController.getById(
        db,
        payoutId
    )


@router.put("/{payoutId}")
def update(
    payoutId: UUID,
    payout: SellerPayoutUpdate,
    db: Session = Depends(getSyncDb)
):
    return sellerPayoutController.update(
        db,
        payoutId,
        payout
    )


@router.delete("/{payoutId}")
def delete(
    payoutId: UUID,
    db: Session = Depends(getSyncDb)
):
    return sellerPayoutController.delete(
        db,
        payoutId
    )