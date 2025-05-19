from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
from integrated_agent.integrated_agent import integrated_agent

app = FastAPI()

chat_history: List[Dict[str, str]] = []

class UserRequest(BaseModel):
    user_input: str

class AgentResponse(BaseModel):
    response: str
    chat_history: List[Dict[str, str]]

@app.post("/chat", response_model=AgentResponse)
def chat(user_request: UserRequest):
    global chat_history
    user_input = user_request.user_input

    try:
        updated_history, response = integrated_agent(user_input, chat_history)

        if user_input.strip().lower() == "exit":
            chat_history = []
        else:
            chat_history = updated_history

        return AgentResponse(response=response, chat_history=chat_history)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return AgentResponse(response=f"Error: {str(e)}", chat_history=chat_history)
