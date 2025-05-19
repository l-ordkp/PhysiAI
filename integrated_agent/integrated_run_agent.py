from rag_agent.run_agent import run_agent

def integrated_run_agent(state):
    state['result'] = run_agent(state['input'])
    return state