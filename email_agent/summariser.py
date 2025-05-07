from utils.llm import llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

def summarise_email(email):
    print("------Summarising the email------")

    system_message = """
    You are an expert email summarizer. Your task is to create concise, accurate summaries of emails that capture:
    1. The main purpose of the email
    2. Any key information, requests, or deadlines
    3. Required actions or next steps

    Format your summary as a 2-3 sentence paragraph. Be direct and clear.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "[Email about a meeting schedule]"),
        ("assistant", "Meeting scheduled for Tuesday, May 10 at 2:00 PM to discuss Q2 marketing strategy. Attendees should review the attached presentation before the meeting and prepare questions. RSVP required by Monday."),
        ("user", "[Email about a product update]"),
        ("assistant", "Summary: New software update (v2.5.1) will be released on Friday with bug fixes and performance improvements. Users should save their work and restart their systems after the update. Technical support will be available for assistance."),
        ("user", "[Email about a payment reminder]"),
        ("assistant", "Summary: Invoice #12345 for $1,250 is overdue by 15 days. Payment is requested immediately via the customer portal, and late fees will apply after May 15. Contact accounting@company.com with any questions."),
        ("user", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()
    summary = chain.invoke({"input": email}).strip().lower()
    summary_cleaned = re.sub(r"<think>.*?</think>", "", summary, flags=re.DOTALL).strip()
    return summary_cleaned