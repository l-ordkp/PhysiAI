from utils.llm import llm
import json
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

def select_event_id(state):
    print("---------Selecting Event ID---------")
    system_message = """You're a calendar assistant. Given a user request and a list of events, choose the best matching event by its event_id.
Respond with only the matching event_id."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", """Input: Delete the project demo
    Events: [{{"summary": "project demo", "event_id": "abc123", "start_time": "2025-05-06T15:00:00"}}]
    Answer: abc123"""),
            ("user", """Input: Change the time of the team sync
    Events: [{{"summary": "team sync", "event_id": "xyz789", "start_time": "2025-05-06T10:00:00"}}]
    Answer: xyz789"""),
            ("user", """Input: {input}
    Events: {events_json}
    Answer:""")
        ])

    events_json = json.dumps(state["events"][:5], indent=2)
    chain = prompt | llm | StrOutputParser()
    best_id = chain.invoke({"input": state["input"], "events_json": events_json})
    cleaned_id = re.sub(r"<think>.*?</think>", "", best_id, flags=re.DOTALL).strip()
    state["event_id"] = cleaned_id.strip().strip('"')
    return state
