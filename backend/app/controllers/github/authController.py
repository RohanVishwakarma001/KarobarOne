from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.userSchema import (
    UserCreate,
    UserLogin,
)
from app.services.github.authService import (
    authService,
)


class AuthController:

    def register(
        self,
        db: Session,
        user: UserCreate
    ):

        createdUser = authService.register(
            db,
            user
        )

        if createdUser is None:
            raise HTTPException(
                status_code=400,
                detail="Email already exists."
            )

        return createdUser

    def login(
        self,
        db: Session,
        user: UserLogin
    ):

        loggedUser = authService.login(
            db,
            user
        )

        if loggedUser is None:
            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        if loggedUser is False:
            raise HTTPException(
                status_code=401,
                detail="Invalid password."
            )

        return {
    "message": "Login successful",
    "user": {
        "id": str(loggedUser.id),
        "first_name": loggedUser.first_name,
        "last_name": loggedUser.last_name,
        "email": loggedUser.email,
        "mobile": loggedUser.mobile,
    }
}


authController = AuthController()