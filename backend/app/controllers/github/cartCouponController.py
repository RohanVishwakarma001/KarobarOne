# ================================================================================
# FILE: controllers/github/cartCouponController.py
# ================================================================================
# Author: Shlok Pallav
# Contact: shlokpallav@gmail.com
# Purpose:
#   Controller layer for Cart Coupon APIs.
# ================================================================================

from fastapi import HTTPException

from app.services.github.cartCouponService import cartCouponService


class CartCouponController:

    def create(self, db, cartCoupon):
        return cartCouponService.create(
            db,
            cartCoupon,
        )

    def getAll(self, db):
        return cartCouponService.getAll(db)

    def getById(self, db, couponId):
        coupon = cartCouponService.getById(
            db,
            couponId,
        )

        if coupon is None:
            raise HTTPException(
                status_code=404,
                detail="Cart Coupon not found",
            )

        return coupon

    def update(
        self,
        db,
        couponId,
        cartCoupon,
    ):
        coupon = cartCouponService.update(
            db,
            couponId,
            cartCoupon,
        )

        if coupon is None:
            raise HTTPException(
                status_code=404,
                detail="Cart Coupon not found",
            )

        return coupon

    def delete(
        self,
        db,
        couponId,
    ):
        deleted = cartCouponService.delete(
            db,
            couponId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Cart Coupon not found",
            )

        return {
            "message": "Cart Coupon deleted successfully"
        }


cartCouponController = CartCouponController()