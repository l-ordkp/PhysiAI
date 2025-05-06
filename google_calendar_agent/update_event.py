from google_calendar_agent.get_calendar_service import get_calendar_service
import datetime
from datetime import datetime, timedelta
import pytz

def update_event(state):
    print("---------Updating Event---------")
    """Update a calendar event with new summary/date/time."""
    service = get_calendar_service()
    event = service.events().get(calendarId='primary', eventId=state['event_id']).execute()
    print(f"State: {state}")

    # Safely access keys with get() method
    if state.get('new_summary'):
        event['summary'] = state.get('new_summary')
    else:
        event['summary'] = state.get('summary', event.get('summary', ''))
        
    # Same pattern for date and time
    new_date = state.get('new_date', state.get('date', ''))
    new_time = state.get('new_time', state.get('time', ''))
    
    ist = pytz.timezone('Asia/Kolkata')
    new_start = ist.localize(datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M"))
    new_end = new_start + timedelta(hours=1)
    event['start'] = {'dateTime': new_start.isoformat(), 'timeZone': 'Asia/Kolkata'}
    event['end'] = {'dateTime': new_end.isoformat(), 'timeZone': 'Asia/Kolkata'}

    updated_event = service.events().update(calendarId='primary', eventId=state['event_id'], body=event).execute()
    state['result'] = "Event updated:" + updated_event.get('htmlLink')
    return state
