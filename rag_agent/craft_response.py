from langchain.prompts import ChatPromptTemplate  
from utils.llm import llm
from typing import Dict
import re
from langchain_core.output_parsers import StrOutputParser 

def craft_response(state: Dict) -> Dict:
    """
    Generates a response using the retrieved context, focusing on Sound Engineering.

    Args:
        state (Dict): The current state of the workflow, containing the query and retrieved context.

    Returns:
        Dict: The updated state with the generated response.
    """
    print("---------craft_response---------")
    system_message = '''You are a sound engineering expert. Use the context provided to answer the user's query. Focus on explaining the details related to audio signal flow, recording techniques, acoustic treatment, sound mixing, mastering, equipment usage, and other relevant sound engineering concepts. Provide clear and technically accurate information to address the user's question.'''
    response_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Query: {query}\nContext: {context}\n\nfeedback: {feedback}")
    ])

    chain = response_prompt | llm| StrOutputParser()
    response = chain.invoke({
        "query": state['query'],
        "context": "\n".join([doc["content"] for doc in state['context']]),
        "feedback": state.get("query_feedback", "") # add feedback to the prompt
    })

    response_re = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    state['response'] = response_re
    print("Response: ", response_re)

    return state