from typing import TypedDict

class AgentState(TypedDict):
    input: str
    intent: str
    events: list
    event_id: str
    output: str
    summary: str
    date: str
    time: str
    new_summary: str
    new_date: str
    new_time: str
    result: str
