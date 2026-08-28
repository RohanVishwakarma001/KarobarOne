from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.savedForLaterRepository import (
    savedForLaterRepository,
)
from app.schemas.github.savedForLaterSchema import (
    SavedForLaterCreate,
    SavedForLaterUpdate,
)


class SavedForLaterService:

    def create(
        self,
        db: Session,
        savedItem: SavedForLaterCreate,
    ):
        return savedForLaterRepository.create(
            db,
            savedItem,
        )

    def getAll(
        self,
        db: Session,
    ):
        return savedForLaterRepository.get_all(db)

    def getById(
        self,
        db: Session,
        savedItemId: UUID,
    ):
        return savedForLaterRepository.get(
            db,
            savedItemId,
            savedForLaterRepository.model.id,
        )

    def update(
        self,
        db: Session,
        savedItemId: UUID,
        savedItem: SavedForLaterUpdate,
    ):
        dbItem = self.getById(
            db,
            savedItemId,
        )

        if dbItem is None:
            return None

        return savedForLaterRepository.update(
            db,
            dbItem,
            savedItem,
        )

    def delete(
        self,
        db: Session,
        savedItemId: UUID,
    ):
        dbItem = self.getById(
            db,
            savedItemId,
        )

        if dbItem is None:
            return False

        savedForLaterRepository.delete(
            db,
            dbItem,
        )

        return True


savedForLaterService = SavedForLaterService()