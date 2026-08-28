from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.productCompareListRepository import (
    productCompareListRepository,
)
from app.schemas.github.productCompareListSchema import (
    ProductCompareListCreate,
)


class ProductCompareListService:

    def create(
        self,
        db: Session,
        compareList: ProductCompareListCreate,
    ):
        return productCompareListRepository.create(
            db,
            compareList,
        )

    def getAll(
        self,
        db: Session,
    ):
        return productCompareListRepository.get_all(db)

    def getById(
        self,
        db: Session,
        compareListId: UUID,
    ):
        return productCompareListRepository.get(
            db,
            compareListId,
            productCompareListRepository.model.id,
        )

    def delete(
        self,
        db: Session,
        compareListId: UUID,
    ):
        dbItem = self.getById(
            db,
            compareListId,
        )

        if dbItem is None:
            return False

        productCompareListRepository.delete(
            db,
            dbItem,
        )

        return True


productCompareListService = ProductCompareListService()