from app.repositories.github.base import BaseRepository
from app.db.models.github.shipmentRequest import ShipmentRequest


class ShipmentRequestRepository(
    BaseRepository[ShipmentRequest]
):

    def __init__(self):

        super().__init__(ShipmentRequest)


shipmentRequestRepository = ShipmentRequestRepository()