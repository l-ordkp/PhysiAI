from utils.llm import llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
import json

def email_body_creator(state):
    print("---------Extracting Event Details---------")

    system_message = f"""You are an AI assistant specialized in extracting email details from user instructions. 
    Your task is to identify the recipient email address, subject line, and email body from the user's input.

    Return ONLY a valid JSON object with these three fields:
    - "recipient_email": The email address of the recipient
    - "subject": The subject line for the email
    - "body": The full body text for the email

    If any information is missing or unclear, use reasonable defaults or ask for clarification."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Input: Send an email to john.doe@example.com about the project deadline. Tell him we need to extend the timeline by two weeks due to the new requirements\nOutput: {{\"recipient_email\": \"john.doe@example.com\", \"subject\": \"Project Deadline Extension\", \"body\": \"Hi John,\n\nI'm writing to inform you that we need to extend the project timeline by two weeks due to the new requirements.\n\nBest regards\"}}"),
        ("user", "Input: {input}\nOutput:")
    ])

    chain = prompt | llm | StrOutputParser()
    raw = chain.invoke({"input": state['input']})
    # Remove <think> tags and parse JSON
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    extracted = json.loads(cleaned)
    state.update(extracted)
    return state
