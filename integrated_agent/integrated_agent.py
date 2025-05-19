from integrated_agent.agent_state import AgentState
from integrated_agent.create_workflow import create_workflow
def integrated_agent(user_input: str, messages: list):
    if user_input.strip().lower() == "exit":
        return [], "Chat history cleared."

    messages.append({"role": "user", "content": user_input})

    graph = create_workflow()
    app = graph.compile()
    initial_state = AgentState(input=user_input)
    final_state = app.invoke(initial_state)

    agent_response = final_state['result']
    messages.append({"role": "agent", "content": agent_response})

    return messages, agent_response


