from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.authController import (
    authController,
)
from app.db.session import getSyncDb
from app.schemas.github.userSchema import (
    UserCreate,
    UserLogin,
    UserResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    db: Session = Depends(getSyncDb)
):
    return authController.register(
        db,
        user
    )


@router.post(
    "/login"
)
def login(
    user: UserLogin,
    db: Session = Depends(getSyncDb)
):
    return authController.login(
        db,
        user
    )