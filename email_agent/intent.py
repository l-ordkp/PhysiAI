from utils.llm import llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

def classify_intent(state):
    print("------Identifying Intent------")

    system_message = """
    You are an AI assistant specialized in identifying user intents from their input. There can be 2 intents 1) send_email and 2) summarise_unread_email.
    Your task is to classify the user's intent based on their input.
    Return ONLY the intent in lowercase without any additional text or explanation.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Can you send an email to John about the meeting"),
        ("assistant", "send_email"),
        ("user", "Can you summarize my unread emails?"),
        ("assistant", "summarise_unread_email"),        
        ("user", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()
    intent = chain.invoke({"input": state["input"]}).strip().lower()
    state["intent"] = re.sub(r"<think>.*?</think>", "", intent, flags=re.DOTALL).strip()
    print("Intent:", state["intent"])
    return state
