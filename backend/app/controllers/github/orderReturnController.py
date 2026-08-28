from fastapi import HTTPException

from app.services.github.orderReturnService import orderReturnService


class OrderReturnController:

    def create(self, db, orderReturn):
        item = orderReturnService.create(db, orderReturn)

        if item is None:
            raise HTTPException(
                status_code=409,
                detail="Return request already exists",
            )

        return item

    def getById(self, db, orderReturnId):
        item = orderReturnService.getById(
            db,
            orderReturnId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Return request not found",
            )

        return item

    def getByOrderId(self, db, orderId):
        item = orderReturnService.getByOrderId(
            db,
            orderId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Return request not found",
            )

        return item

    def update(
        self,
        db,
        orderReturnId,
        orderReturn,
    ):
        item = orderReturnService.update(
            db,
            orderReturnId,
            orderReturn,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Return request not found",
            )

        return item

    def delete(self, db, orderReturnId):
        deleted = orderReturnService.delete(
            db,
            orderReturnId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Return request not found",
            )

        return {
            "message": "Return request deleted successfully"
        }


orderReturnController = OrderReturnController()