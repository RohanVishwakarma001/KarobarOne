# ================================================================================
# FILE: api/v1/endpoints/github/cartCouponRouter.py
# ================================================================================
# Author: Shlok Pallav
# Contact: shlokpallav@gmail.com
# Purpose:
#   Cart Coupon API endpoints.
# ================================================================================

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.cartCouponController import cartCouponController
from app.db.session import getSyncDb
from app.schemas.github.cartCouponSchema import (
    CartCouponCreate,
    CartCouponUpdate,
    CartCouponResponse,
)

router = APIRouter(
    prefix="/cart-coupons",
    tags=["Cart Coupons"],
)


@router.post(
    "/",
    response_model=CartCouponResponse,
    status_code=201,
)
def createCartCoupon(
    cartCoupon: CartCouponCreate,
    db: Session = Depends(getSyncDb),
):
    return cartCouponController.create(
        db,
        cartCoupon,
    )


@router.get(
    "/",
    response_model=List[CartCouponResponse],
)
def getCartCoupons(
    db: Session = Depends(getSyncDb),
):
    return cartCouponController.getAll(db)


@router.get(
    "/{couponId}",
    response_model=CartCouponResponse,
)
def getCartCoupon(
    couponId: UUID,
    db: Session = Depends(getSyncDb),
):
    return cartCouponController.getById(
        db,
        couponId,
    )


@router.put(
    "/{couponId}",
    response_model=CartCouponResponse,
)
def updateCartCoupon(
    couponId: UUID,
    cartCoupon: CartCouponUpdate,
    db: Session = Depends(getSyncDb),
):
    return cartCouponController.update(
        db,
        couponId,
        cartCoupon,
    )


@router.delete(
    "/{couponId}",
)
def deleteCartCoupon(
    couponId: UUID,
    db: Session = Depends(getSyncDb),
):
    return cartCouponController.delete(
        db,
        couponId,
    )