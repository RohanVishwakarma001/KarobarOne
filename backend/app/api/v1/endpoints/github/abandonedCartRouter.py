from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.abandonedCartController import (
    abandonedCartController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    AbandonedCartCreate,
    AbandonedCartUpdate,
    AbandonedCartResponse,
)

router = APIRouter(
    prefix="/abandoned-carts",
    tags=["Abandoned Carts"],
)


@router.post("/", response_model=AbandonedCartResponse, status_code=201)
def createAbandonedCart(
    abandonedCart: AbandonedCartCreate,
    db: Session = Depends(getSyncDb),
):
    return abandonedCartController.create(
        db,
        abandonedCart,
    )


@router.get("/", response_model=list[AbandonedCartResponse])
def getAbandonedCarts(
    db: Session = Depends(getSyncDb),
):
    return abandonedCartController.getAll(db)


@router.get("/{abandonedCartId}", response_model=AbandonedCartResponse)
def getAbandonedCart(
    abandonedCartId: UUID,
    db: Session = Depends(getSyncDb),
):
    return abandonedCartController.getById(
        db,
        abandonedCartId,
    )


@router.put("/{abandonedCartId}", response_model=AbandonedCartResponse)
def updateAbandonedCart(
    abandonedCartId: UUID,
    abandonedCart: AbandonedCartUpdate,
    db: Session = Depends(getSyncDb),
):
    return abandonedCartController.update(
        db,
        abandonedCartId,
        abandonedCart,
    )


@router.delete("/{abandonedCartId}")
def deleteAbandonedCart(
    abandonedCartId: UUID,
    db: Session = Depends(getSyncDb),
):
    return abandonedCartController.delete(
        db,
        abandonedCartId,
    )