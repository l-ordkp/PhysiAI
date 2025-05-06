from __future__ import print_function
import datetime
from google_calendar_agent.get_calendar_service import get_calendar_service

def create_event(state):
    """
    Creates a calendar event.

    Args:
        summary: The name of the event.
        date: The date of the event in YYYY-MM-DD format.
        time: The start time in HH:MM (24-hour format).

    Returns:
        Confirmation of the event creation.
    """
    print("---------Creating Event---------")
    service = get_calendar_service()

    start_datetime = f"{state['date']}T{state['time']}:00"
    end_time = (datetime.datetime.strptime(state['time'], "%H:%M") + datetime.timedelta(hours=1)).strftime("%H:%M")
    end_datetime = f"{state['date']}T{end_time}:00"

    event = {
        'summary': state['summary'],
        'location': 'Online',
        'description': f'Event:',
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': True,
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    state['result']= "Event created at:" + event.get('htmlLink')
    return state

