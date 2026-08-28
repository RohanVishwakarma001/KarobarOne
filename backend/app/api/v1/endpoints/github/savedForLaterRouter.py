from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.savedForLaterController import (
    savedForLaterController,
)
from app.db.session import getSyncDb
from app.schemas.github.savedForLaterSchema import (
    SavedForLaterCreate,
    SavedForLaterUpdate,
    SavedForLaterResponse,
)

router = APIRouter(
    prefix="/saved-for-later",
    tags=["Saved For Later"],
)


@router.post(
    "/",
    response_model=SavedForLaterResponse,
    status_code=201,
)
def createSavedItem(
    savedItem: SavedForLaterCreate,
    db: Session = Depends(getSyncDb),
):
    return savedForLaterController.create(
        db,
        savedItem,
    )


@router.get(
    "/",
    response_model=list[SavedForLaterResponse],
)
def getSavedItems(
    db: Session = Depends(getSyncDb),
):
    return savedForLaterController.getAll(db)


@router.get(
    "/{savedItemId}",
    response_model=SavedForLaterResponse,
)
def getSavedItem(
    savedItemId: UUID,
    db: Session = Depends(getSyncDb),
):
    return savedForLaterController.getById(
        db,
        savedItemId,
    )


@router.put(
    "/{savedItemId}",
    response_model=SavedForLaterResponse,
)
def updateSavedItem(
    savedItemId: UUID,
    savedItem: SavedForLaterUpdate,
    db: Session = Depends(getSyncDb),
):
    return savedForLaterController.update(
        db,
        savedItemId,
        savedItem,
    )


@router.delete(
    "/{savedItemId}",
)
def deleteSavedItem(
    savedItemId: UUID,
    db: Session = Depends(getSyncDb),
):
    return savedForLaterController.delete(
        db,
        savedItemId,
    )