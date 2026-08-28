from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    CouponCreate,
    CouponUpdate,
)
from app.services.github.couponService import couponService


class CouponController:

    def create(
        self,
        db: Session,
        coupon: CouponCreate,
    ):
        return couponService.create(
            db,
            coupon,
        )

    def getAll(
        self,
        db: Session,
    ):
        return couponService.getAll(db)

    def getById(
        self,
        db: Session,
        couponId: UUID,
    ):
        coupon = couponService.getById(
            db,
            couponId,
        )

        if coupon is None:
            raise HTTPException(
                status_code=404,
                detail="Coupon not found",
            )

        return coupon

    def update(
        self,
        db: Session,
        couponId: UUID,
        coupon: CouponUpdate,
    ):
        updatedCoupon = couponService.update(
            db,
            couponId,
            coupon,
        )

        if updatedCoupon is None:
            raise HTTPException(
                status_code=404,
                detail="Coupon not found",
            )

        return updatedCoupon

    def delete(
        self,
        db: Session,
        couponId: UUID,
    ):
        deleted = couponService.delete(
            db,
            couponId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Coupon not found",
            )

        return {
            "message": "Coupon deleted successfully"
        }


couponController = CouponController()