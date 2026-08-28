from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.couponRepository import couponRepository
from app.schemas.github.schemas import CouponCreate, CouponUpdate


class CouponService:

    def create(
        self,
        db: Session,
        coupon: CouponCreate,
    ):
        return couponRepository.create(
            db,
            coupon,
        )

    def getAll(
        self,
        db: Session,
    ):
        return couponRepository.get_all(db)

    def getById(
        self,
        db: Session,
        couponId: UUID,
    ):
        return couponRepository.get(
            db,
            couponId,
            couponRepository.model.id,
        )

    def update(
        self,
        db: Session,
        couponId: UUID,
        coupon: CouponUpdate,
    ):
        dbCoupon = self.getById(
            db,
            couponId,
        )

        if dbCoupon is None:
            return None

        return couponRepository.update(
            db,
            dbCoupon,
            coupon,
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

        couponRepository.delete(
            db,
            dbCoupon,
        )

        return True


couponService = CouponService()