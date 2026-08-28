from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.sellerPayoutSchema import (
    SellerPayoutCreate,
    SellerPayoutUpdate,
)
from app.services.github.sellerPayoutService import (
    sellerPayoutService,
)


class SellerPayoutController:

    def create(
        self,
        db: Session,
        payout: SellerPayoutCreate
    ):
        return sellerPayoutService.create(
            db,
            payout
        )

    def getAll(
        self,
        db: Session
    ):
        return sellerPayoutService.getAll(db)

    def getById(
        self,
        db: Session,
        payoutId: UUID
    ):
        payout = sellerPayoutService.getById(
            db,
            payoutId
        )

        if payout is None:
            raise HTTPException(
                status_code=404,
                detail="Seller payout not found."
            )

        return payout

    def update(
        self,
        db: Session,
        payoutId: UUID,
        payout: SellerPayoutUpdate
    ):
        dbPayout = sellerPayoutService.update(
            db,
            payoutId,
            payout
        )

        if dbPayout is None:
            raise HTTPException(
                status_code=404,
                detail="Seller payout not found."
            )

        return dbPayout

    def delete(
        self,
        db: Session,
        payoutId: UUID
    ):
        deleted = sellerPayoutService.delete(
            db,
            payoutId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Seller payout not found."
            )

        return {
            "message": "Seller payout deleted successfully."
        }


sellerPayoutController = SellerPayoutController()