from utils.llm import llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

def classify_intent(state):
    print("------Identifying Intent------")

    system_message = """
    You are a smart calendar assistant. Based on the user's input, classify the user's intent into one of the following categories:
    - "create": if the user wants to create a new event.
    - "update": if the user wants to update an existing event (like changing time/date/summary).
    - "delete": if the user wants to delete an event.
    - "list": if the user wants to see a list of events.

    Respond with only one word: create, update, delete, or list.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Add meeting with Alice at 3pm tomorrow."),
        ("assistant", "create"),
        ("user", "Schedule a dentist appointment on May 10th."),
        ("assistant", "create"),
        ("user", "Change my lunch with Bob to 2pm."),
        ("assistant", "update"),
        ("user", "Reschedule my yoga session to next Friday."),
        ("assistant", "update"),
        ("user", "Delete my call with John."),
        ("assistant", "delete"),
        ("user", "Cancel the gym session."),
        ("assistant", "delete"),
        ("user", "What do I have scheduled this week?"),
        ("assistant", "list"),
        ("user", "Show all upcoming events."),
        ("assistant", "list"),
        ("user", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()
    intent = chain.invoke({"input": state["input"]}).strip().lower()
    state["intent"] = re.sub(r"<think>.*?</think>", "", intent, flags=re.DOTALL).strip()
    print("Intent:", state["intent"])
    return state
