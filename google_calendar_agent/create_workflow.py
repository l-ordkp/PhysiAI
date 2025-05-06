from langgraph.graph import StateGraph, END
from google_calendar_agent.classify_intent import classify_intent
from google_calendar_agent.extract_event_details import extract_event_details
from google_calendar_agent.create_event import create_event
from google_calendar_agent.list_of_events import list_of_events
from google_calendar_agent.select_event_id import select_event_id
from google_calendar_agent.update_event import update_event
from google_calendar_agent.delete_event import delete_event
from google_calendar_agent.agent_state import AgentState
from google_calendar_agent.router_decision import router_decision

def create_workflow():
# Build the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("extract_event_details", extract_event_details)
    workflow.add_node("create_event", create_event)
    workflow.add_node("list_of_events", list_of_events)
    workflow.add_node("select_event_id", select_event_id)
    workflow.add_node("update_event", update_event)
    workflow.add_node("delete_event", delete_event)

    # Set entry point
    workflow.set_entry_point("extract_event_details")
    workflow.add_edge("extract_event_details", "classify_intent")
    # Conditional edge from classify_intent → based on intent
    workflow.add_conditional_edges(
        "classify_intent",
        router_decision,
        path_map={
            "create_event": "create_event",
            "list_of_events": "list_of_events",
            "end": END
        }
    )

    # Route to update or delete
    def decide_update_or_delete(state):
        return state["intent"]

    workflow.add_conditional_edges(
        "list_of_events",
        decide_update_or_delete,
        path_map={
            "update": "select_event_id",
            "delete": "select_event_id",
            "list": END
        }
    )

    workflow.add_conditional_edges(
        "select_event_id",
        decide_update_or_delete,
        path_map={
            "update": "update_event",
            "delete": "delete_event"
        }
    )
    # Finalize update/delete path
    workflow.add_edge("update_event", END)
    workflow.add_edge("delete_event", END)
    return workflow
