from google_calendar_agent.get_calendar_service import get_calendar_service
from datetime import datetime, timezone


def list_of_events(state):
    """List events from a given date (YYYY-MM-DD) onward with summary, event_id, and start_time."""
    
    start_datetime = datetime.strptime(state['date'], "%Y-%m-%d").replace(tzinfo=timezone.utc).isoformat()
    print(f"Start datetime: {start_datetime}")
    service = get_calendar_service()
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_datetime,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    
    if not events:
        return []

    state['events'] = [
        {
            "summary": e.get("summary", "No Title"),
            "event_id": e["id"],
            "start_time": e.get("start", {}).get("dateTime") or e.get("start", {}).get("date", "")
        }
        for e in events
    ]
    if state['intent'] == "list":
        state['result'] = str(state['events'])
        return state
    else:
        return state
