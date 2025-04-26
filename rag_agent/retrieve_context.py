from utils.vector_store import VectorStore
vector_store = VectorStore()

def retrieve_context(state):
    """
    Retrieves context from the vector store using the expanded or original query.

    Args:
        state (Dict): The current state of the workflow, containing the query and expanded query.

    Returns:
        Dict: The updated state with the retrieved context.
    """
    print("---------retrieve_context---------")
    query = state['expanded_query']  # Complete the code to define the key for the expanded query
    #print("Query used for retrieval:", query)  # Debugging: Print the query

    # Retrieve documents from the vector store
    docs = vector_store.retrieve_content_from_query(query)
    
    state['retrieved_context'] = docs  # Complete the code to define the key for storing the context
    print("Extracted context:", docs)  # Debugging: Print the extracted context
    #print(f"Groundedness loop count: {state['groundedness_loop_count']}")
    return state
