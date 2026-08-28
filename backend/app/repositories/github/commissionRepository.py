# Owner: shlokpallav@gmail.com

from sqlalchemy.orm import Session

from app.db.models.github.order import Order


class CommissionRepository:

    def getById(
        self,
        db: Session,
        orderId,
    ) -> Order | None:

        return (
            db.query(Order)
            .filter(Order.id == orderId)
            .first()
        )


commissionRepository = CommissionRepository()