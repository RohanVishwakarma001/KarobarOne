from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.couponController import couponController
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    CouponCreate,
    CouponUpdate,
    CouponResponse,
)

router = APIRouter(
    prefix="/coupons",
    tags=["Coupons"],
)


@router.post(
    "/",
    response_model=CouponResponse,
    status_code=201,
)
def createCoupon(
    coupon: CouponCreate,
    db: Session = Depends(getSyncDb),
):
    return couponController.create(
        db,
        coupon,
    )


@router.get(
    "/",
    response_model=list[CouponResponse],
)
def getCoupons(
    db: Session = Depends(getSyncDb),
):
    return couponController.getAll(db)


@router.get(
    "/{couponId}",
    response_model=CouponResponse,
)
def getCoupon(
    couponId: UUID,
    db: Session = Depends(getSyncDb),
):
    return couponController.getById(
        db,
        couponId,
    )


@router.put(
    "/{couponId}",
    response_model=CouponResponse,
)
def updateCoupon(
    couponId: UUID,
    coupon: CouponUpdate,
    db: Session = Depends(getSyncDb),
):
    return couponController.update(
        db,
        couponId,
        coupon,
    )


@router.delete(
    "/{couponId}",
)
def deleteCoupon(
    couponId: UUID,
    db: Session = Depends(getSyncDb),
):
    return couponController.delete(
        db,
        couponId,
    )