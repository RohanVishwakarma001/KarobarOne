from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.couponRedemptionController import (
    couponRedemptionController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    CouponRedemptionCreate,
    CouponRedemptionUpdate,
    CouponRedemptionResponse,
)

router = APIRouter(
    prefix="/coupon-redemptions",
    tags=["Coupon Redemptions"],
)


@router.post(
    "/",
    response_model=CouponRedemptionResponse,
    status_code=201,
)
def createCouponRedemption(
    redemption: CouponRedemptionCreate,
    db: Session = Depends(getSyncDb),
):
    return couponRedemptionController.create(
        db,
        redemption,
    )


@router.get(
    "/",
    response_model=list[CouponRedemptionResponse],
)
def getCouponRedemptions(
    db: Session = Depends(getSyncDb),
):
    return couponRedemptionController.getAll(db)


@router.get(
    "/{redemptionId}",
    response_model=CouponRedemptionResponse,
)
def getCouponRedemption(
    redemptionId: UUID,
    db: Session = Depends(getSyncDb),
):
    return couponRedemptionController.getById(
        db,
        redemptionId,
    )


@router.put(
    "/{redemptionId}",
    response_model=CouponRedemptionResponse,
)
def updateCouponRedemption(
    redemptionId: UUID,
    redemption: CouponRedemptionUpdate,
    db: Session = Depends(getSyncDb),
):
    return couponRedemptionController.update(
        db,
        redemptionId,
        redemption,
    )


@router.delete(
    "/{redemptionId}",
)
def deleteCouponRedemption(
    redemptionId: UUID,
    db: Session = Depends(getSyncDb),
):
    return couponRedemptionController.delete(
        db,
        redemptionId,
    )