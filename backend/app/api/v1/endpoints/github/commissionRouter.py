# Owner: shlokpallav@gmail.com

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.github.commissionController import (
    commissionController,
)
from app.db.session import getSyncDb
from app.schemas.github.commissionSchema import (
    CommissionRequest,
    CommissionResponse,
)

router = APIRouter(
    prefix="/commission",
    tags=["Commission"],
)


@router.post(
    "/calculate",
    response_model=CommissionResponse,
    status_code=status.HTTP_200_OK,
)
def calculateCommission(
    request: CommissionRequest,
    db: Session = Depends(getSyncDb),
):
    return commissionController.calculateCommission(
        db=db,
        request=request,
    )