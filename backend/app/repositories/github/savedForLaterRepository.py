from app.db.models.github.models import SavedForLater
from app.repositories.github.base import BaseRepository


class SavedForLaterRepository(BaseRepository[SavedForLater]):

    def __init__(self):
        super().__init__(SavedForLater)


savedForLaterRepository = SavedForLaterRepository()