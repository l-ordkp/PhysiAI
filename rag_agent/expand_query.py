from langchain.prompts import ChatPromptTemplate  
from utils.llm import llm
from langchain_core.output_parsers import StrOutputParser 
import re
def expand_query(state):
    """
    Expands the user query to improve retrieval of sound engineering information.

    Args:
        state (Dict): The current state of the workflow, containing the user query.

    Returns:
        Dict: The updated state with the expanded query.
    """
    print("---------Expanding Query---------")
    system_message = '''You are an expert in sound engineering and audio technology. Based on the user query, expand it to include related details  
    about concepts such as audio signal flow, equipment usage, acoustic treatment, mixing and mastering techniques,  
    common challenges, and relevant terminology. The goal is to enhance the query with broader technical context while staying focused on sound engineering and audio production. Remeber you only have to expand the query and not provide the answer.
    '''

    expand_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Expand this query: {query} using the feedback: {query_feedback}")

    ])

    chain = expand_prompt | llm | StrOutputParser()
    expanded_query = chain.invoke({"query": state['query'], "query_feedback":state["query_feedback"]})
    
    expanded_query_re = re.sub(r"<think>.*?</think>", "", expanded_query, flags=re.DOTALL).strip()
    print("expanded_query", expanded_query_re)
    state["expanded_query"] = expanded_query_re
    return state
