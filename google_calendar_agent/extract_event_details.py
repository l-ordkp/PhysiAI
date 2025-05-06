from utils.llm import llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
from datetime import datetime
import json

def extract_event_details(state):
    print("---------Extracting Event Details---------")
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    system_message = f"""You are a calendar assistant that can extracts all the info regarding the calendar event. Today's date is {current_date} and the current time is {current_time}.
    Interpret relative phrases like "today", "tomorrow", or "next Friday" accordingly. Do not leave any field blank.
    Extract and return a JSON object with any available of the following:
    - "summary": original event title being referred to
    - "date": original event date
    - "time": original event time
    - "new_summary": new event title if the user wants to rename the event or change the title
    - "new_date": new event date if the user wants to reschedule the event
    - "new_time: new event time if the user wants to reschedule the event"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Input: Schedule a meeting with Alice on 2025-05-07 at 15:00\nOutput: {{\"summary\": \"meeting with Alice\", \"date\": \"2025-05-07\", \"time\": \"15:00\"}}"),
        ("user", "Input: Add interview to calendar tomorrow at 2pm\nOutput: {{\"summary\": \"interview\", \"date\": \"2025-05-07\", \"time\": \"14:00\"}}"),
        ("user", "Input: Reschedule 'Team Sync' to 2025-05-09 at 15:00\nOutput: {{\"summary\": \"Team Sync\", \"new_date\": \"2025-05-09\", \"new_time\": \"15:00\"}}"),
        ("user", "Input: Rename 'Demo call' to 'Client Discussion'\nOutput: {{\"summary\": \"Demo call\", \"new_summary\": \"Client Discussion\"}}"),
        ("user", "Input: Delete 'Weekly Meeting' from tomorrow\nOutput: {{\"summary\": \"Weekly Meeting\", \"date\": \"2025-05-07\"}}"),
        ("user", "Input: {input}\nOutput:")
    ])

    chain = prompt | llm | StrOutputParser()
    raw = chain.invoke({"input": state["input"]})

    # Remove <think> tags and parse JSON
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    extracted = json.loads(cleaned)
    state.update(extracted)
    print(f"Extracted details: {state}")
    return state
