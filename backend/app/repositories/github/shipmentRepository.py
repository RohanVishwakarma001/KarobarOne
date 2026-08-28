from app.repositories.github.base import BaseRepository
from app.db.models.github.shipment import Shipment


class ShipmentRepository(
    BaseRepository[Shipment]
):

    def __init__(self):

        super().__init__(Shipment)


shipmentRepository = ShipmentRepository()