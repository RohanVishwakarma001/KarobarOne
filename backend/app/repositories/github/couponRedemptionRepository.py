from app.db.models.github.models import CouponRedemption
from app.repositories.github.base import BaseRepository


class CouponRedemptionRepository(BaseRepository[CouponRedemption]):

    def __init__(self):
        super().__init__(CouponRedemption)


couponRedemptionRepository = CouponRedemptionRepository()