from langchain.prompts import ChatPromptTemplate  
from rag_agent.agent_state import llm
from langchain_core.output_parsers import StrOutputParser 
from typing import Dict

def refine_response(state: Dict) -> Dict:
    """
    Suggests improvements for the generated response.

    Args:
        state (Dict): The current state of the workflow, containing the query and response.

    Returns:
        Dict: The updated state with response refinement suggestions.
    """
    print("---------refine_response---------")

    system_message = '''You are tasked with suggesting improvements for the given response to enhance its accuracy and completeness.
    Focus on making sure the response is directly related to the query and includes all relevant information.
    The suggestions should be specific, actionable, and aimed at improving the quality of the response.'''

    refine_response_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Query: {query}\nResponse: {response}\n\n"
                 "What improvements can be made to enhance accuracy and completeness?")
    ])

    chain = refine_response_prompt | llm| StrOutputParser()

    # Store response suggestions in a structured format
    feedback = f"Previous Response: {state['response']}\nSuggestions: {chain.invoke({'query': state['query'], 'response': state['response']})}"
    print("feedback: ", feedback)
    print(f"State: {state}")
    state['feedback'] = feedback
    return state