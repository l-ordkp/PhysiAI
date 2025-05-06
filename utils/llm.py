from langchain_groq import ChatGroq
import os
llm = ChatGroq(temperature=0,model_name="qwen-qwq-32b",api_key=os.getenv("GROQ_API_KEY"))