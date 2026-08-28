
from app.db.models.github.models import Coupon
from app.repositories.github.base import BaseRepository


class CouponRepository(BaseRepository[Coupon]):

    def __init__(self):
        super().__init__(Coupon)


couponRepository = CouponRepository()