from app.db.models.github.models import OrderCancellation
from app.repositories.github.base import BaseRepository

orderCancellationRepository = BaseRepository(OrderCancellation)