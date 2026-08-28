from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    CouponRedemptionCreate,
    CouponRedemptionUpdate,
)
from app.services.github.couponRedemptionService import (
    couponRedemptionService,
)


class CouponRedemptionController:

    def create(
        self,
        db: Session,
        redemption: CouponRedemptionCreate,
    ):
        return couponRedemptionService.create(
            db,
            redemption,
        )

    def getAll(
        self,
        db: Session,
    ):
        return couponRedemptionService.getAll(db)

    def getById(
        self,
        db: Session,
        redemptionId: UUID,
    ):
        item = couponRedemptionService.getById(
            db,
            redemptionId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Coupon Redemption not found",
            )

        return item

    def update(
        self,
        db: Session,
        redemptionId: UUID,
        redemption: CouponRedemptionUpdate,
    ):
        item = couponRedemptionService.update(
            db,
            redemptionId,
            redemption,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Coupon Redemption not found",
            )

        return item

    def delete(
        self,
        db: Session,
        redemptionId: UUID,
    ):
        deleted = couponRedemptionService.delete(
            db,
            redemptionId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Coupon Redemption not found",
            )

        return {
            "message": "Coupon Redemption deleted successfully"
        }


couponRedemptionController = CouponRedemptionController()