from typing import Dict
def max_iterations_reached(state: Dict) -> Dict:
    """Handles the case when the maximum number of iterations is reached."""
    print("---------max_iterations_reached---------")
    """Handles the case when the maximum number of iterations is reached."""
    response = "I'm unable to refine the response further. Please provide more context or clarify your question."
    state['response'] = response
    return state
