from utils.llm import llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

def classify_intent(state):
    print("------Identifying Intent Category------")

    system_message = """
    You are an AI assistant specialized in categorizing user intents. Classify the user's input into exactly ONE of these four categories:
    
    1) email - For requests related to emails such as sending emails, reading emails, summarizing unread emails, etc.
    2) calendar - For Google Calendar activities like scheduling events, updating events, deleting events, or displaying event lists.
    3) rag - For questions specifically related to the physics concept of sound .
    4) other - For any requests that don't fit into the above three categories.
    
    Return ONLY the category name in lowercase without any additional text or explanation.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Can you send an email to John about the meeting"),
        ("assistant", "email"),
        ("user", "Schedule a team meeting for next Tuesday at 3pm"),
        ("assistant", "calendar"),
        ("user", "What's the difference between dynamic and condenser microphones?"),
        ("assistant", "rag"),
        ("user", "What's the weather like today?"),
        ("assistant", "other"),
        ("user", "Summarize my unread emails"),
        ("assistant", "email"),
        ("user", "Delete my 2pm appointment"),
        ("assistant", "calendar"),
        ("user", "How do I properly set up a compressor for vocals?"),
        ("assistant", "rag"),
        ("user", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()
    category = chain.invoke({"input": state["input"]}).strip().lower()
    state["intent"] = re.sub(r"<think>.*?</think>", "", category, flags=re.DOTALL).strip()
    print("Intent Category:", state["intent"])
    return state
