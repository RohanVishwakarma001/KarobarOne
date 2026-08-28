from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.offerRepository import offerRepository
from app.schemas.github.schemas import OfferCreate, OfferUpdate


class OfferService:

    def create(
        self,
        db: Session,
        offer: OfferCreate,
    ):
        return offerRepository.create(db, offer)

    def getAll(
        self,
        db: Session,
    ):
        return offerRepository.get_all(db)

    def getById(
        self,
        db: Session,
        offerId: UUID,
    ):
        return offerRepository.get(
            db,
            offerId,
            offerRepository.model.id,
        )

    def update(
        self,
        db: Session,
        offerId: UUID,
        offer: OfferUpdate,
    ):
        dbOffer = self.getById(db, offerId)

        if dbOffer is None:
            return None

        return offerRepository.update(
            db,
            dbOffer,
            offer,
        )

    def delete(
        self,
        db: Session,
        offerId: UUID,
    ):
        dbOffer = self.getById(db, offerId)

        if dbOffer is None:
            return False

        offerRepository.delete(
            db,
            dbOffer,
        )

        return True


offerService = OfferService()