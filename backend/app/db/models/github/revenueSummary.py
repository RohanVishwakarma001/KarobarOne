import uuid

from sqlalchemy import Column, Date, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class RevenueSummary(BaseGithub):

    __tablename__ = "revenue_summary"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    report_month = Column(
        Date,
        nullable=False
    )

    subscription_revenue = Column(
        Numeric(10, 2),
        default=0
    )

    commission_revenue = Column(
        Numeric(10, 2),
        default=0
    )

    total_revenue = Column(
        Numeric(10, 2),
        default=0
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )