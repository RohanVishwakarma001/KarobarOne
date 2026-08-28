from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.productCompareItemController import (
    productCompareItemController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    ProductCompareItemCreate,
    ProductCompareItemResponse,
)

router = APIRouter(
    prefix="/product-compare-items",
    tags=["Product Compare Items"],
)


@router.post(
    "/",
    response_model=ProductCompareItemResponse,
    status_code=201,
)
def createProductCompareItem(
    compareItem: ProductCompareItemCreate,
    db: Session = Depends(getSyncDb),
):
    return productCompareItemController.create(
        db,
        compareItem,
    )


@router.get(
    "/",
    response_model=list[ProductCompareItemResponse],
)
def getProductCompareItems(
    db: Session = Depends(getSyncDb),
):
    return productCompareItemController.getAll(
        db,
    )


@router.get(
    "/{compareItemId}",
    response_model=ProductCompareItemResponse,
)
def getProductCompareItem(
    compareItemId: UUID,
    db: Session = Depends(getSyncDb),
):
    return productCompareItemController.getById(
        db,
        compareItemId,
    )


@router.delete(
    "/{compareItemId}",
)
def deleteProductCompareItem(
    compareItemId: UUID,
    db: Session = Depends(getSyncDb),
):
    return productCompareItemController.delete(
        db,
        compareItemId,
    )