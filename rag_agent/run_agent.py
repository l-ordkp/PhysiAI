from rag_agent.create_workflow import create_workflow
from utils.img_retrieve import retrieve_image

def run_agent(user_input: str):
    # Step 1: Build the workflow
    graph = create_workflow()

    # Step 2: Compile the graph
    app = graph.compile()

    # Step 3: Define the initial state
    intial_state = {
        "query": user_input,  # Current user query
        "expanded_query": "",  # Complete the code to define the expanded version of the query
        "context": [],  # Retrieved documents (initially empty)
        "response": "",  # Complete the code to define the AI-generated response
        "precision_score": 0.0,  # Complete the code to define the precision score of the response
        "groundedness_score": 0.0,  # Complete the code to define the groundedness score of the response
        "groundedness_loop_count": 0,  # Complete the code to define the counter for groundedness loops
        "precision_loop_count": 0,  # Complete the code to define the counter for precision loops
        "feedback": "",  # Complete the code to define the feedback
        "query_feedback": "",  # Complete the code to define the query feedback
        "loop_max_iter": 5  # Complete the code to define the maximum number of iterations for loops
    }
    final_state = app.invoke(intial_state)
    img_path = retrieve_image(user_input)
    answer = f'The answer to your question is: {final_state["response"]}. The best image suitable for your question is: {img_path}.'
    return answer

