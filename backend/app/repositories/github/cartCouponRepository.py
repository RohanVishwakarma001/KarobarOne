# ================================================================================
# FILE: repositories/github/cartCouponRepository.py
# ================================================================================
# Author: Shlok Pallav
# Contact: shlokpallav@gmail.com
# Purpose:
#   Repository layer for Cart Coupon CRUD operations.
# ================================================================================

from app.db.models.github.models import CartCoupon
from app.repositories.github.base import BaseRepository


class CartCouponRepository(BaseRepository[CartCoupon]):

    def __init__(self):
        super().__init__(CartCoupon)


cartCouponRepository = CartCouponRepository()