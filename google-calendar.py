import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build


class Event:
    summary: str
    description: str
    start_date: str


def get_event() -> Event:
    load_dotenv(".env", override=True)

    SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
    GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")
    SEARCH_TERMS = os.getenv("SEARCH_TERMS")
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build("calendar", "v3", credentials=credentials)

    min = datetime.now() - timedelta(days=1)
    events_result = (
        service.events()
        .list(
            calendarId=GOOGLE_CALENDAR_ID,
            timeMin=min.strftime('%Y-%m-%dT%H:%M:%SZ'),
            maxResults=1,
            singleEvents=True,
            orderBy="startTime",
            q=SEARCH_TERMS
        )
        .execute()
    )

    events = events_result["items"]
    if len(events) == 0:
        raise LookupError("No events found.")

    event = Event()
    event.summary = events[0]["summary"]
    event.description = events[0]["description"]
    event.start_date = events[0]["start"]["date"]

    return event


if __name__ == "__main__":
    get_event()
