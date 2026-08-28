from fastapi import APIRouter

from app.services.github.calendarService import calendarService

router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"]
)


@router.get("/")
def test():
    return {
        "message": "Calendar Router Working"
    }


@router.get("/login")
def login():
    return {
        "auth_url": calendarService.get_login_url()
    }


@router.get("/callback")
def callback(code: str):

    token = calendarService.save_token(code)

    return {
        "message": "Calendar Connected",
        "access_token": token.get("access_token"),
    }