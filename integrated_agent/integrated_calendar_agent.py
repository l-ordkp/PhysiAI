from google_calendar_agent.google_cal_agent import calendar_agent

def integrated_calendar_agent(state):
    state['result'] = calendar_agent(state['input'])
    return state