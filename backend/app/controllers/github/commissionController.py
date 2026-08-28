# Owner: shlokpallav@gmail.com

from sqlalchemy.orm import Session

from app.schemas.github.commissionSchema import (
    CommissionRequest,
    CommissionResponse,
)
from app.services.github.commissionService import (
    commissionService,
)


class CommissionController:

    def calculateCommission(
        self,
        db: Session,
        request: CommissionRequest,
    ) -> CommissionResponse:

        return commissionService.calculateCommission(
            db=db,
            request=request,
        )


commissionController = CommissionController()