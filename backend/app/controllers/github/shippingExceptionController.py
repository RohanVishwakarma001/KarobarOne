from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.shippingExceptionSchema import (
    ShippingExceptionCreate,
    ShippingExceptionUpdate,
)

from app.services.github.shippingExceptionService import (
    shippingExceptionService,
)


class ShippingExceptionController:

    def create(
        self,
        db: Session,
        shippingException: ShippingExceptionCreate
    ):

        return shippingExceptionService.create(
            db,
            shippingException
        )

    def getAll(
        self,
        db: Session
    ):

        return shippingExceptionService.getAll(db)

    def getById(
        self,
        db: Session,
        shippingExceptionId: UUID
    ):

        shippingException = shippingExceptionService.getById(
            db,
            shippingExceptionId
        )

        if shippingException is None:

            raise HTTPException(
                status_code=404,
                detail="Shipping Exception not found."
            )

        return shippingException

    def update(
        self,
        db: Session,
        shippingExceptionId: UUID,
        shippingException: ShippingExceptionUpdate
    ):

        updatedException = shippingExceptionService.update(
            db,
            shippingExceptionId,
            shippingException
        )

        if updatedException is None:

            raise HTTPException(
                status_code=404,
                detail="Shipping Exception not found."
            )

        return updatedException

    def delete(
        self,
        db: Session,
        shippingExceptionId: UUID
    ):

        deleted = shippingExceptionService.delete(
            db,
            shippingExceptionId
        )

        if not deleted:

            raise HTTPException(
                status_code=404,
                detail="Shipping Exception not found."
            )

        return {
            "message": "Shipping Exception deleted successfully."
        }


shippingExceptionController = ShippingExceptionController()