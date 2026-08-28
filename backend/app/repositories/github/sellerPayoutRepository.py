from app.db.models.github.sellerPayout import SellerPayout
from app.repositories.github.base import BaseRepository


class SellerPayoutRepository(
    BaseRepository[SellerPayout]
):

    def __init__(self):

        super().__init__(SellerPayout)


sellerPayoutRepository = SellerPayoutRepository()