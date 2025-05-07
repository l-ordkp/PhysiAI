from email_agent.agent_state import AgentState
from email_agent.create_workflow import create_workflow

def email_agent(user_input: str):
    # Step 1: Build the workflow
    graph = create_workflow()

    # Step 2: Compile the graph
    app = graph.compile()

    # Step 3: Define the initial state
    initial_state = AgentState(input=user_input)
    print(f"Initial state: {initial_state}")
    
    # Step 4: Run the agent
    final_state = app.invoke(initial_state)
    
    return final_state['result']

