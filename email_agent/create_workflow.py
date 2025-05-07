from langgraph.graph import StateGraph, END
from email_agent.intent import classify_intent
from email_agent.email_sender import email_sender
from email_agent.unread_email_summariser import unread_email_summariser
from email_agent.agent_state import AgentState
from email_agent.router_decision import router_decision

def create_workflow():
    # Build the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("email_sender", email_sender)
    workflow.add_node("router_decision", router_decision)
    workflow.add_node("unread_email_summariser", unread_email_summariser)

    # Set entry point
    workflow.set_entry_point("classify_intent")

    # Conditional edge from classify_intent → based on intent
    workflow.add_conditional_edges(
        "classify_intent",
        router_decision,
        path_map={
            "send_email": "email_sender",
            "summarise_unread_emails": "unread_email_summariser",
            "end": END
        }
    )

    workflow.add_edge("email_sender", END)
    workflow.add_edge("unread_email_summariser", END)
    return workflow