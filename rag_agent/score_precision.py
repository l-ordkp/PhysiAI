from langchain.prompts import ChatPromptTemplate  
from utils.llm import llm
from langchain_core.output_parsers import BaseOutputParser
from typing import Dict
import re

class FloatOutputParser(BaseOutputParser):
    def parse(self, text: str) -> float:
        # Remove <think>...</think> block if it exists
        text_without_think = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        
        # Now clean and strip it
        cleaned_text = text_without_think.strip()
        
        # Finally convert to float
        return float(cleaned_text)


def check_precision(state: Dict) -> Dict:
    """
    Checks whether the response precisely addresses the user’s query.

    Args:
        state (Dict): The current state of the workflow, containing the query and response.

    Returns:
        Dict: The updated state with the precision score.
    """
    print("---------check_precision---------")
    system_message = '''
    You are tasked with determining whether the given response precisely addresses the user's query.
    The response should directly and accurately answer the question posed in the query without deviating from the topic.
    Please return a score between 0 and 1, where 1 indicates a precise answer and 0 indicates an imprecise or irrelevant answer.

    Here are some examples:

    Example 1:
    Query: "What is the capital of France?"
    Response: "The capital of France is Paris."
    Score: 1 (Precise and fully answers the question)

    Example 2:
    Query: "How many continents are there?"
    Response: "There are seven continents on Earth."
    Score: 1 (Precise and fully answers the question)

    Example 3:
    Query: "What is photosynthesis?"
    Response: "Photosynthesis is the process by which plants convert sunlight into chemical energy."
    Score: 1 (Precise and fully answers the question)

    Example 4:
    Query: "What is the capital of France?"
    Response: "France is a country in Europe with beautiful landmarks."
    Score: 0.5 (Partially related but does not directly answer the query)

    Example 5:
    Query: "How many continents are there?"
    Response: "The oceans cover about 70 percent of Earth's surface."
    Score: 0 (Irrelevant — does not answer the query)

    Be concise. Just return the numerical score (like 0, 0.5, or 1) based on your evaluation.
    '''
    # Create the precision prompt

    precision_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Query: {query}\nResponse: {response}\n\nPrecision score:")
    ])

    chain = precision_prompt | llm | FloatOutputParser() # Complete the code to define the chain of processing
    precision_score = chain.invoke({
        "query": state['query'],
        "response":state['response'] # Complete the code to access the response from the state
    })
   
    state['precision_score'] = precision_score
    print("precision_score:", precision_score)
    state['precision_loop_count'] +=1
    print("#########Precision Incremented###########")
    return state