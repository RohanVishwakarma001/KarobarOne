from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.productCompareListController import (
    productCompareListController,
)
from app.db.session import getSyncDb
from app.schemas.github.productCompareListSchema import (
    ProductCompareListCreate,
    ProductCompareListResponse,
)

router = APIRouter(
    prefix="/product-compare-lists",
    tags=["Product Compare Lists"],
)


@router.post(
    "/",
    response_model=ProductCompareListResponse,
    status_code=201,
)
def createProductCompareList(
    compareList: ProductCompareListCreate,
    db: Session = Depends(getSyncDb),
):
    return productCompareListController.create(
        db,
        compareList,
    )


@router.get(
    "/",
    response_model=list[ProductCompareListResponse],
)
def getProductCompareLists(
    db: Session = Depends(getSyncDb),
):
    return productCompareListController.getAll(db)


@router.get(
    "/{compareListId}",
    response_model=ProductCompareListResponse,
)
def getProductCompareList(
    compareListId: UUID,
    db: Session = Depends(getSyncDb),
):
    return productCompareListController.getById(
        db,
        compareListId,
    )


@router.delete(
    "/{compareListId}",
)
def deleteProductCompareList(
    compareListId: UUID,
    db: Session = Depends(getSyncDb),
):
    return productCompareListController.delete(
        db,
        compareListId,
    )