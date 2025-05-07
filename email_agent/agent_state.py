from typing import TypedDict

class AgentState(TypedDict):
    input: str
    intent: str
    result: list
    receipent_email: str
    subject: str
    body: str
    
