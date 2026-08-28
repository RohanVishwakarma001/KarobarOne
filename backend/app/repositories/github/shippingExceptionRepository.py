from app.repositories.github.base import BaseRepository
from app.db.models.github.shippingException import ShippingException


class ShippingExceptionRepository(
    BaseRepository[ShippingException]
):

    def __init__(self):

        super().__init__(ShippingException)


shippingExceptionRepository = ShippingExceptionRepository()