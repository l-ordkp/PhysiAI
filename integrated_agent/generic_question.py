from utils.llm import llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

def generic_question(state):
    print("------Identifying Intent Category------")

    system_message = """
    You are an AI assistant meant to answer generic question of the users.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()
    category = chain.invoke({"input": state["input"]}).strip().lower()
    state["result"] = re.sub(r"<think>.*?</think>", "", category, flags=re.DOTALL).strip()
    print("Answer", state["result"])
    return state
