from typing import TypedDict

class AgentState(TypedDict):
    input: str
    intent: str
    result: str

    