from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.shippingExceptionRepository import (
    shippingExceptionRepository,
)

from app.schemas.github.shippingExceptionSchema import (
    ShippingExceptionCreate,
    ShippingExceptionUpdate,
)


class ShippingExceptionService:

    def create(
        self,
        db: Session,
        shippingException: ShippingExceptionCreate
    ):

        return shippingExceptionRepository.create(
            db=db,
            obj=shippingException
        )

    def getAll(
        self,
        db: Session
    ):

        return shippingExceptionRepository.get_all(db)

    def getById(
        self,
        db: Session,
        shippingExceptionId: UUID
    ):

        return shippingExceptionRepository.get(
            db=db,
            obj_id=shippingExceptionId,
            id_field=shippingExceptionRepository.model.id
        )

    def update(
        self,
        db: Session,
        shippingExceptionId: UUID,
        shippingException: ShippingExceptionUpdate
    ):

        dbException = self.getById(
            db,
            shippingExceptionId
        )

        if dbException is None:
            return None

        return shippingExceptionRepository.update(
            db=db,
            db_obj=dbException,
            obj=shippingException
        )

    def delete(
        self,
        db: Session,
        shippingExceptionId: UUID
    ):

        dbException = self.getById(
            db,
            shippingExceptionId
        )

        if dbException is None:
            return False

        shippingExceptionRepository.delete(
            db=db,
            db_obj=dbException
        )

        return True


shippingExceptionService = ShippingExceptionService()