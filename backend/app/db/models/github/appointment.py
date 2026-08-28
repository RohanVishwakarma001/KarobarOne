import uuid

from sqlalchemy import Column, Date, DateTime, String, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class Appointment(BaseGithub):

    __tablename__ = "appointments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_name = Column(
        String(255),
        nullable=False
    )

    customer_phone = Column(
        String(20)
    )

    customer_email = Column(
        String(255)
    )

    service_name = Column(
        String(255),
        nullable=False
    )

    appointment_date = Column(
        Date,
        nullable=False
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
        nullable=False
    )

    google_event_link = Column(
        String(500)
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )