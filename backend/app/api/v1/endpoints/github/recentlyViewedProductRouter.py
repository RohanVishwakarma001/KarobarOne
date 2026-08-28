from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.recentlyViewedProductController import (
    recentlyViewedProductController,
)
from app.db.session import getSyncDb
from app.schemas.github.recentlyViewedProductSchema import (
    RecentlyViewedProductCreate,
    RecentlyViewedProductResponse,
)

router = APIRouter(
    prefix="/recently-viewed-products",
    tags=["Recently Viewed Products"],
)


@router.post(
    "/",
    response_model=RecentlyViewedProductResponse,
    status_code=201,
)
def createRecentlyViewedProduct(
    view: RecentlyViewedProductCreate,
    db: Session = Depends(getSyncDb),
):
    return recentlyViewedProductController.create(
        db,
        view,
    )


@router.get(
    "/",
    response_model=list[RecentlyViewedProductResponse],
)
def getRecentlyViewedProducts(
    db: Session = Depends(getSyncDb),
):
    return recentlyViewedProductController.getAll(db)


@router.get(
    "/{recentlyViewedId}",
    response_model=RecentlyViewedProductResponse,
)
def getRecentlyViewedProduct(
    recentlyViewedId: UUID,
    db: Session = Depends(getSyncDb),
):
    return recentlyViewedProductController.getById(
        db,
        recentlyViewedId,
    )


@router.delete(
    "/{recentlyViewedId}",
)
def deleteRecentlyViewedProduct(
    recentlyViewedId: UUID,
    db: Session = Depends(getSyncDb),
):
    return recentlyViewedProductController.delete(
        db,
        recentlyViewedId,
    )