from uuid import UUID


from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.savedForLaterSchema import (
    SavedForLaterCreate,
    SavedForLaterUpdate,
)
from app.services.github.savedForLaterService import (
    savedForLaterService,
)


class SavedForLaterController:

    def create(
        self,
        db: Session,
        savedItem: SavedForLaterCreate,
    ):
        return savedForLaterService.create(
            db,
            savedItem,
        )

    def getAll(
        self,
        db: Session,
    ):
        return savedForLaterService.getAll(db)

    def getById(
        self,
        db: Session,
        savedItemId: UUID,
    ):
        item = savedForLaterService.getById(
            db,
            savedItemId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Saved item not found",
            )

        return item

    def update(
        self,
        db: Session,
        savedItemId: UUID,
        savedItem: SavedForLaterUpdate,
    ):
        item = savedForLaterService.update(
            db,
            savedItemId,
            savedItem,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Saved item not found",
            )

        return item

    def delete(
        self,
        db: Session,
        savedItemId: UUID,
    ):
        deleted = savedForLaterService.delete(
            db,
            savedItemId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Saved item not found",
            )

        return {
            "message": "Item removed successfully"
        }


savedForLaterController = SavedForLaterController()