from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    AbandonedCartCreate,
    AbandonedCartUpdate,
)
from app.services.github.abandonedCartService import (
    abandonedCartService,
)


class AbandonedCartController:

    def create(self, db: Session, abandonedCart: AbandonedCartCreate):
        return abandonedCartService.create(db, abandonedCart)

    def getAll(self, db: Session):
        return abandonedCartService.getAll(db)

    def getById(self, db: Session, abandonedCartId: UUID):
        cart = abandonedCartService.getById(db, abandonedCartId)

        if cart is None:
            raise HTTPException(
                status_code=404,
                detail="Abandoned Cart not found",
            )

        return cart

    def update(
        self,
        db: Session,
        abandonedCartId: UUID,
        abandonedCart: AbandonedCartUpdate,
    ):
        cart = abandonedCartService.update(
            db,
            abandonedCartId,
            abandonedCart,
        )

        if cart is None:
            raise HTTPException(
                status_code=404,
                detail="Abandoned Cart not found",
            )

        return cart

    def delete(
        self,
        db: Session,
        abandonedCartId: UUID,
    ):
        deleted = abandonedCartService.delete(
            db,
            abandonedCartId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Abandoned Cart not found",
            )

        return {
            "message": "Abandoned cart deleted successfully"
        }


abandonedCartController = AbandonedCartController()