from datetime import date, datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class AppointmentCreate(BaseModel):

    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    service_name: str
    appointment_date: date
    start_time: time
    end_time: time


class AppointmentUpdate(BaseModel):

    appointment_date: date
    start_time: time
    end_time: time


class AppointmentResponse(BaseModel):

    id: UUID
    customer_name: str
    customer_phone: Optional[str]
    customer_email: Optional[EmailStr]
    service_name: str
    appointment_date: date
    start_time: time
    end_time: time
    google_event_link: Optional[str]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )