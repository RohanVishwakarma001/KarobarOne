from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.github.appointment import Appointment
from app.repositories.github.appointmentRepository import appointmentRepository
from app.schemas.github.appointmentSchema import (
    AppointmentCreate,
    AppointmentUpdate,
)
from app.services.github.calendarService import calendarService


class AppointmentService:

    def create(
        self,
        db: Session,
        appointment: AppointmentCreate
    ):

        if appointment.end_time <= appointment.start_time:
            raise HTTPException(
                status_code=400,
                detail="End time must be after start time."
            )

        existing = db.query(Appointment).filter(
            Appointment.appointment_date == appointment.appointment_date,
            Appointment.start_time == appointment.start_time
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Time slot already booked."
            )

        start_datetime = (
            f"{appointment.appointment_date}T{appointment.start_time}+05:30"
        )

        end_datetime = (
            f"{appointment.appointment_date}T{appointment.end_time}+05:30"
        )

        event_link = calendarService.create_event(
            summary=f"{appointment.service_name} - {appointment.customer_name}",
            description=f"{appointment.customer_email}",
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

        data = appointment.model_dump(mode="json")
        data["google_event_link"] = event_link

        db_obj = Appointment(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def getAll(
        self,
        db: Session
    ):
        return appointmentRepository.get_all(db)

    def getById(
        self,
        db: Session,
        appointmentId
    ):
        return appointmentRepository.get(
            db=db,
            obj_id=appointmentId,
            id_field=appointmentRepository.model.id
        )

    def update(
        self,
        db: Session,
        appointmentId,
        appointment: AppointmentUpdate
    ):
        dbAppointment = self.getById(
            db,
            appointmentId
        )

        if dbAppointment is None:
            return None

        return appointmentRepository.update(
            db=db,
            db_obj=dbAppointment,
            obj=appointment
        )

    def delete(
        self,
        db: Session,
        appointmentId
    ):
        dbAppointment = self.getById(
            db,
            appointmentId
        )

        if dbAppointment is None:
            return False

        appointmentRepository.delete(
            db=db,
            db_obj=dbAppointment
        )

        return True


appointmentService = AppointmentService()