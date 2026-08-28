from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.appointmentController import appointmentController
from app.db.session import getSyncDb
from app.schemas.github.appointmentSchema import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=201
)
def createAppointment(
    appointment: AppointmentCreate,
    db: Session = Depends(getSyncDb)
):
    return appointmentController.create(
        db,
        appointment
    )


@router.get(
    "/",
    response_model=List[AppointmentResponse]
)
def getAppointments(
    db: Session = Depends(getSyncDb)
):
    return appointmentController.getAll(db)


@router.get(
    "/{appointmentId}",
    response_model=AppointmentResponse
)
def getAppointment(
    appointmentId: UUID,
    db: Session = Depends(getSyncDb)
):
    return appointmentController.getById(
        db,
        appointmentId
    )


@router.put(
    "/{appointmentId}",
    response_model=AppointmentResponse
)
def updateAppointment(
    appointmentId: UUID,
    appointment: AppointmentUpdate,
    db: Session = Depends(getSyncDb)
):
    return appointmentController.update(
        db,
        appointmentId,
        appointment
    )


@router.delete(
    "/{appointmentId}"
)
def deleteAppointment(
    appointmentId: UUID,
    db: Session = Depends(getSyncDb)
):
    return appointmentController.delete(
        db,
        appointmentId
    )