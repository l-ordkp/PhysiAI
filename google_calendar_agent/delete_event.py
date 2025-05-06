from google_calendar_agent.get_calendar_service import get_calendar_service

def delete_event(state):
    """Delete a calendar event using its event_id."""
    service = get_calendar_service()
    service.events().delete(calendarId='primary', eventId=state['event_id']).execute()
    state['result'] ="Event with ID" + state['event_id']+ "deleted"
    return state

