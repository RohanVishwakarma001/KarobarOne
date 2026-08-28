from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.productCompareListSchema import (
    ProductCompareListCreate,
)
from app.services.github.productCompareListService import (
    productCompareListService,
)

class ProductCompareListController:

    def create(
        self,
        db: Session,
        compareList: ProductCompareListCreate,
    ):
        return productCompareListService.create(
            db,
            compareList,
        )

    def getAll(
        self,
        db: Session,
    ):
        return productCompareListService.getAll(db)

    def getById(
        self,
        db: Session,
        compareListId: UUID,
    ):
        item = productCompareListService.getById(
            db,
            compareListId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Product Compare List not found",
            )

        return item

    def delete(
        self,
        db: Session,
        compareListId: UUID,
    ):
        deleted = productCompareListService.delete(
            db,
            compareListId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Product Compare List not found",
            )

        return {
            "message": "Product Compare List deleted successfully"
        }


productCompareListController = ProductCompareListController()