from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.offerTargetRepository import (
    offerTargetRepository,
)
from app.schemas.github.schemas import (
    OfferTargetCreate,
)


class OfferTargetService:

    def create(
        self,
        db: Session,
        target: OfferTargetCreate,
    ):
        return offerTargetRepository.create(
            db,
            target,
        )

    def getAll(
        self,
        db: Session,
    ):
        return offerTargetRepository.get_all(db)

    def getById(
        self,
        db: Session,
        targetId: UUID,
    ):
        return offerTargetRepository.get(
            db,
            targetId,
            offerTargetRepository.model.id,
        )

    def delete(
        self,
        db: Session,
        targetId: UUID,
    ):
        dbTarget = self.getById(
            db,
            targetId,
        )

        if dbTarget is None:
            return False

        offerTargetRepository.delete(
            db,
            dbTarget,
        )

        return True


offerTargetService = OfferTargetService()