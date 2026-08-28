from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.sellerPayoutRepository import (
    sellerPayoutRepository,
)
from app.schemas.github.sellerPayoutSchema import (
    SellerPayoutCreate,
    SellerPayoutUpdate,
)


class SellerPayoutService:

    def create(
        self,
        db: Session,
        payout: SellerPayoutCreate
    ):
        return sellerPayoutRepository.create(
            db=db,
            obj=payout
        )

    def getAll(
        self,
        db: Session
    ):
        return sellerPayoutRepository.get_all(db)

    def getById(
        self,
        db: Session,
        payoutId: UUID
    ):
        return sellerPayoutRepository.get(
            db=db,
            obj_id=payoutId,
            id_field=sellerPayoutRepository.model.id
        )

    def update(
        self,
        db: Session,
        payoutId: UUID,
        payout: SellerPayoutUpdate
    ):
        dbPayout = self.getById(
            db,
            payoutId
        )

        if dbPayout is None:
            return None

        return sellerPayoutRepository.update(
            db=db,
            db_obj=dbPayout,
            obj=payout
        )

    def delete(
        self,
        db: Session,
        payoutId: UUID
    ):
        dbPayout = self.getById(
            db,
            payoutId
        )

        if dbPayout is None:
            return False

        sellerPayoutRepository.delete(
            db=db,
            db_obj=dbPayout
        )

        return True


sellerPayoutService = SellerPayoutService()