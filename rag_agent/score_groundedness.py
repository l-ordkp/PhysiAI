from langchain.prompts import ChatPromptTemplate  
from rag_agent.agent_state import llm
from typing import Dict
from langchain_core.output_parsers import BaseOutputParser
import re  

class FloatOutputParser(BaseOutputParser):
    def parse(self, text: str) -> float:
        # Remove <think>...</think> block if it exists
        text_without_think = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        
        # Now clean and strip it
        cleaned_text = text_without_think.strip()
        
        # Finally convert to float
        return float(cleaned_text)
    
def score_groundedness(state: Dict) -> Dict:
    print("---------check_groundedness---------")
    
    system_message = '''
    You are tasked with determining whether the given response is grounded in the context provided.
    ... [examples] ...
    Be concise. Just return the numerical score (like 0, 0.5, or 1) based on your evaluation.
    '''

    groundedness_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "Context: {context}\nResponse: {response}\n\nGroundedness score:")
    ])

    chain = groundedness_prompt | llm | FloatOutputParser()

    groundedness_score = chain.invoke({
        "context": "\n".join([doc["content"] for doc in state['context']]),
        "response": state['response']
    })

    print("groundedness_score: ", groundedness_score)

    state['groundedness_loop_count'] += 1
    print("#########Groundedness Incremented###########")
    state['groundedness_score'] = groundedness_score

    return state
