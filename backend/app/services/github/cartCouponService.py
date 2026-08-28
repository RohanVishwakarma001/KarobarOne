# ================================================================================
# FILE: services/github/cartCouponService.py
# ================================================================================
# Author: Shlok Pallav
# Contact: shlokpallav@gmail.com
# Purpose:
#   Business logic layer for Cart Coupon operations.
# ================================================================================

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.cartCouponRepository import cartCouponRepository
from app.schemas.github.cartCouponSchema import (
    CartCouponCreate,
    CartCouponUpdate,
)


class CartCouponService:

    def create(
        self,
        db: Session,
        cartCoupon: CartCouponCreate,
    ):
        return cartCouponRepository.create(
            db=db,
            obj=cartCoupon,
        )

    def getAll(
        self,
        db: Session,
    ):
        return cartCouponRepository.get_all(db)

    def getById(
        self,
        db: Session,
        couponId: UUID,
    ):
        return cartCouponRepository.get(
            db=db,
            obj_id=couponId,
            id_field=cartCouponRepository.model.id,
        )

    def update(
        self,
        db: Session,
        couponId: UUID,
        cartCoupon: CartCouponUpdate,
    ):
        dbCoupon = self.getById(
            db,
            couponId,
        )

        if dbCoupon is None:
            return None

        return cartCouponRepository.update(
            db=db,
            db_obj=dbCoupon,
            obj=cartCoupon,
        )

    def delete(
        self,
        db: Session,
        couponId: UUID,
    ):
        dbCoupon = self.getById(
            db,
            couponId,
        )

        if dbCoupon is None:
            return False

        cartCouponRepository.delete(
            db=db,
            db_obj=dbCoupon,
        )

        return True


cartCouponService = CartCouponService()