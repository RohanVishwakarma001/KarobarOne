# Owner: shlokpallav@gmail.com

from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.github.commissionRepository import (
    commissionRepository,
)
from app.schemas.github.commissionSchema import (
    CommissionRequest,
    CommissionResponse,
)


class CommissionService:

    def calculateCommission(
        self,
        db: Session,
        request: CommissionRequest,
    ) -> CommissionResponse:

        order = commissionRepository.getById(
            db=db,
            orderId=request.order_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        commissionAmount = (
            request.order_amount
            * request.commission_percentage
            / Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        sellerAmount = (
            request.order_amount
            - commissionAmount
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        return CommissionResponse(
            order_id=request.order_id,
            order_amount=request.order_amount,
            commission_percentage=request.commission_percentage,
            commission_amount=commissionAmount,
            seller_amount=sellerAmount,
            message="Commission calculated successfully.",
        )


commissionService = CommissionService()