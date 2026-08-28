from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.abandonedCartRepository import (
    abandonedCartRepository,
)
from app.schemas.github.schemas import (
    AbandonedCartCreate,
    AbandonedCartUpdate,
)


class AbandonedCartService:

    def create(
        self,
        db: Session,
        abandonedCart: AbandonedCartCreate,
    ):
        return abandonedCartRepository.create(
            db,
            abandonedCart,
        )

    def getAll(
        self,
        db: Session,
    ):
        return abandonedCartRepository.get_all(db)

    def getById(
        self,
        db: Session,
        abandonedCartId: UUID,
    ):
        return abandonedCartRepository.get(
            db,
            abandonedCartId,
            abandonedCartRepository.model.id,
        )

    def update(
        self,
        db: Session,
        abandonedCartId: UUID,
        abandonedCart: AbandonedCartUpdate,
    ):
        dbCart = self.getById(
            db,
            abandonedCartId,
        )

        if dbCart is None:
            return None

        return abandonedCartRepository.update(
            db,
            dbCart,
            abandonedCart,
        )

    def delete(
        self,
        db: Session,
        abandonedCartId: UUID,
    ):
        dbCart = self.getById(
            db,
            abandonedCartId,
        )

        if dbCart is None:
            return False

        abandonedCartRepository.delete(
            db,
            dbCart,
        )

        return True


abandonedCartService = AbandonedCartService()