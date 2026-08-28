import os

import requests
from dotenv import load_dotenv
from fastapi import HTTPException
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

SCOPES = "https://www.googleapis.com/auth/calendar"

saved_credentials = {}


class CalendarService:

    def get_login_url(self):

        return (
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={GOOGLE_REDIRECT_URI}"
            "&response_type=code"
            f"&scope={SCOPES}"
            "&access_type=offline"
            "&prompt=consent"
        )

    def save_token(self, code: str):

        token_url = "https://oauth2.googleapis.com/token"

        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=response.json()
            )

        token = response.json()

        saved_credentials["token"] = token.get("access_token")
        saved_credentials["refresh_token"] = token.get("refresh_token")
        saved_credentials["token_uri"] = "https://oauth2.googleapis.com/token"
        saved_credentials["client_id"] = GOOGLE_CLIENT_ID
        saved_credentials["client_secret"] = GOOGLE_CLIENT_SECRET
        saved_credentials["scopes"] = [SCOPES]

        return token

    def create_event(
        self,
        summary,
        description,
        start_datetime,
        end_datetime,
    ):

        if not saved_credentials:
            return None

        credentials = Credentials(
            token=saved_credentials["token"],
            refresh_token=saved_credentials["refresh_token"],
            token_uri=saved_credentials["token_uri"],
            client_id=saved_credentials["client_id"],
            client_secret=saved_credentials["client_secret"],
            scopes=saved_credentials["scopes"],
        )

        service = build(
            "calendar",
            "v3",
            credentials=credentials
        )

        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_datetime,
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": "Asia/Kolkata",
            },
        }

        created = service.events().insert(
            calendarId="primary",
            body=event
        ).execute()

        return created.get("htmlLink")


calendarService = CalendarService()