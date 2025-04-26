from langchain.prompts import ChatPromptTemplate  
from rag_agent.agent_state import llm
from langchain_core.output_parsers import StrOutputParser 
from typing import Dict
def refine_query(state: Dict) -> Dict:
    """
    Suggests improvements for the expanded query.

    Args:
        state (Dict): The current state of the workflow, containing the query and expanded query.

    Returns:
        Dict: The updated state with query refinement suggestions.
    """
    print("---------refine_query---------")
    system_message = '''You are tasked with suggesting improvements for the expanded query to enhance its effectiveness for a search.
    The goal is to improve the query in a way that it provides more relevant results, is clear, and is specific enough for accurate retrieval.
    Provide actionable suggestions for improving the query.'''

    refine_query_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Original Query: {query}\nExpanded Query: {expanded_query}\n\n"
                 "What improvements can be made for a better search?")
    ])

    chain = refine_query_prompt | llm | StrOutputParser()

    # Store refinement suggestions without modifying the original expanded query
    query_feedback = f"Previous Expanded Query: {state['expanded_query']}\nSuggestions: {chain.invoke({'query': state['query'], 'expanded_query': state['expanded_query']})}"
    print("query_feedback: ", query_feedback)
    print(f"Groundedness loop count: {state['groundedness_loop_count']}")
    state['query_feedback'] = query_feedback
    return state
