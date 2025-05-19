from email_agent.complete_email_agent import complete_mail_agent

def integrated_email_agent(state):
    state['result']= complete_mail_agent(state['input'])
    return state