from rag_agent.expand_query import expand_query
from rag_agent.retrieve_context import retrieve_context
from rag_agent.craft_response import craft_response
from rag_agent.score_groundedness import score_groundedness
from rag_agent.refine_response import refine_response
from rag_agent.score_precision import check_precision
from rag_agent.refine_query import refine_query
from rag_agent.max_iterations_reached import max_iterations_reached
from rag_agent.should_continue_groundedness import should_continue_groundedness
from rag_agent.should_continue_precision import should_continue_precision
from rag_agent.agent_state import AgentState
from langgraph.graph import END, StateGraph, START

def create_workflow() -> StateGraph:
    """Creates the updated workflow for the RAG agent."""
    workflow = StateGraph(AgentState)

    # Add processing nodes
    workflow.add_node("expand_query", expand_query)         # Step 1: Expand user query.
    workflow.add_node("retrieve_context", retrieve_context) # Step 2: Retrieve relevant documents.
    workflow.add_node("craft_response", craft_response)     # Step 3: Generate a response based on retrieved data.
    workflow.add_node("score_groundedness", score_groundedness)  # Step 4: Evaluate response grounding.
    workflow.add_node("refine_response", refine_response)   # Step 5: Improve response if it's weakly grounded.
    workflow.add_node("check_precision", check_precision)   # Step 6: Evaluate response precision.
    workflow.add_node("refine_query", refine_query)         # Step 7: Improve query if response lacks precision.
    workflow.add_node("max_iterations_reached", max_iterations_reached)  # Step 8: Handle max iterations.
    # Main flow edges
    workflow.add_edge(START, "expand_query")
    workflow.add_edge("expand_query", "retrieve_context")
    workflow.add_edge("retrieve_context", "craft_response")
    workflow.add_edge("craft_response", "score_groundedness")



    # Conditional edges based on groundedness check
    workflow.add_conditional_edges(
        "score_groundedness",
        should_continue_groundedness,  # Use the conditional function
        {
            "check_precision": "check_precision",  # If well-grounded, proceed to precision check.
            "refine_query": "refine_query",  # If not, refine the response.
            "max_iterations_reached": "max_iterations_reached"  # If max loops reached, exit.
        }
    )
    workflow.add_edge("refine_response", "craft_response")  # Refined responses are reprocessed.

    # Conditional edges based on precision check
    workflow.add_conditional_edges(
        "check_precision",
        should_continue_precision,  # Use the conditional function
        {
            "pass": END,              # If precise, complete the workflow.
            "refine_response": "refine_response",  # If imprecise, refine the query.
            "max_iterations_reached": "max_iterations_reached"  # If max loops reached, exit.
        }
    )
    workflow.add_edge("refine_query", "expand_query")  # Refined queries go through expansion again.

    workflow.add_edge("max_iterations_reached", END)

    return workflow