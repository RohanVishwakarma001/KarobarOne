from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.offerExclusionRepository import (
    offerExclusionRepository,
)
from app.schemas.github.schemas import (
    OfferExclusionCreate,
    OfferExclusionUpdate,
)


class OfferExclusionService:

    def create(
        self,
        db: Session,
        exclusion: OfferExclusionCreate,
    ):
        return offerExclusionRepository.create(
            db,
            exclusion,
        )

    def getAll(
        self,
        db: Session,
    ):
        return offerExclusionRepository.get_all(db)

    def getById(
        self,
        db: Session,
        exclusionId: UUID,
    ):
        return offerExclusionRepository.get(
            db,
            exclusionId,
            offerExclusionRepository.model.id,
        )

    def update(
        self,
        db: Session,
        exclusionId: UUID,
        exclusion: OfferExclusionUpdate,
    ):
        dbItem = self.getById(
            db,
            exclusionId,
        )

        if dbItem is None:
            return None

        return offerExclusionRepository.update(
            db,
            dbItem,
            exclusion,
        )

    def delete(
        self,
        db: Session,
        exclusionId: UUID,
    ):
        dbItem = self.getById(
            db,
            exclusionId,
        )

        if dbItem is None:
            return False

        offerExclusionRepository.delete(
            db,
            dbItem,
        )

        return True


offerExclusionService = OfferExclusionService()