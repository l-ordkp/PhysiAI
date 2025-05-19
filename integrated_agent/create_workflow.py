from langgraph.graph import StateGraph, END
from integrated_agent.router_decision import router_decision
from integrated_agent.integrated_email_agent import integrated_email_agent
from integrated_agent.integrated_calendar_agent import integrated_calendar_agent
from integrated_agent.integrated_run_agent import integrated_run_agent
from integrated_agent.agent_state import AgentState
from integrated_agent.intent import classify_intent
from integrated_agent.generic_question import generic_question

def create_workflow():
    # Build the graph
    workflow = StateGraph(AgentState)
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("email_agent", integrated_email_agent)
    workflow.add_node("rag_agent",integrated_run_agent)
    workflow.add_node("calendar_agent", integrated_calendar_agent)
    workflow.add_node("router_decision", router_decision)
    workflow.add_node("generic_question", generic_question)

    workflow.set_entry_point("classify_intent")
    workflow.add_conditional_edges(
        "classify_intent",
        router_decision,
        path_map={
            "email": "email_agent",
            "calendar": "calendar_agent",
            "rag": "rag_agent",
            "other": "generic_question"
        }
    )
    workflow.add_edge("email_agent", END)
    workflow.add_edge("calendar_agent", END)
    workflow.add_edge("rag_agent", END)
    workflow.add_edge("generic_question", END)
    return workflow


