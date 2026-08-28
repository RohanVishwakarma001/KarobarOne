from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.appointmentSchema import (
    AppointmentCreate,
    AppointmentUpdate,
)
from app.services.github.appointmentService import appointmentService


class AppointmentController:

    def create(
        self,
        db: Session,
        appointment: AppointmentCreate
    ):
        return appointmentService.create(
            db,
            appointment
        )

    def getAll(
        self,
        db: Session
    ):
        return appointmentService.getAll(db)

    def getById(
        self,
        db: Session,
        appointmentId
    ):
        appointment = appointmentService.getById(
            db,
            appointmentId
        )

        if appointment is None:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found."
            )

        return appointment

    def update(
        self,
        db: Session,
        appointmentId,
        appointment: AppointmentUpdate
    ):
        updated = appointmentService.update(
            db,
            appointmentId,
            appointment
        )

        if updated is None:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found."
            )

        return updated

    def delete(
        self,
        db: Session,
        appointmentId
    ):
        deleted = appointmentService.delete(
            db,
            appointmentId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found."
            )

        return {
            "message": "Appointment deleted successfully."
        }


appointmentController = AppointmentController()