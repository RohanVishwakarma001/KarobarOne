from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.couponRedemptionRepository import (
    couponRedemptionRepository,
)
from app.schemas.github.schemas import (
    CouponRedemptionCreate,
    CouponRedemptionUpdate,
)


class CouponRedemptionService:

    def create(
        self,
        db: Session,
        redemption: CouponRedemptionCreate,
    ):
        return couponRedemptionRepository.create(
            db,
            redemption,
        )

    def getAll(
        self,
        db: Session,
    ):
        return couponRedemptionRepository.get_all(db)

    def getById(
        self,
        db: Session,
        redemptionId: UUID,
    ):
        return couponRedemptionRepository.get(
            db,
            redemptionId,
            couponRedemptionRepository.model.id,
        )

    def update(
        self,
        db: Session,
        redemptionId: UUID,
        redemption: CouponRedemptionUpdate,
    ):
        dbItem = self.getById(
            db,
            redemptionId,
        )

        if dbItem is None:
            return None

        return couponRedemptionRepository.update(
            db,
            dbItem,
            redemption,
        )

    def delete(
        self,
        db: Session,
        redemptionId: UUID,
    ):
        dbItem = self.getById(
            db,
            redemptionId,
        )

        if dbItem is None:
            return False

        couponRedemptionRepository.delete(
            db,
            dbItem,
        )

        return True


couponRedemptionService = CouponRedemptionService()