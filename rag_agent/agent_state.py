import os
from langchain_groq import ChatGroq
from typing import TypedDict, List, Dict, Any
from dotenv import load_dotenv
load_dotenv()
class AgentState(TypedDict):
    query: str  # The current user query
    expanded_query: str  # The expanded version of the user query
    context: List[Dict[str, Any]]  # Retrieved documents (content and metadata)
    response: str  # The generated response to the user query
    precision_score: float  # The precision score of the response
    groundedness_score: float  # The groundedness score of the response
    groundedness_loop_count: int  # Counter for groundedness refinement loops
    precision_loop_count: int  # Counter for precision refinement loops
    feedback: str  # Feedback from the user
    query_feedback: str  # Feedback specifically related to the query
    groundedness_check: bool  # Indicator for groundedness check
    loop_max_iter: int  # Maximum iterations for loops

llm = ChatGroq(temperature=0,model_name="qwen-qwq-32b",api_key=os.getenv("GROQ_API_KEY"))