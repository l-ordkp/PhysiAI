from typing import Dict
def should_continue_precision(state: Dict) -> str:
    """Decides if precision is sufficient or needs improvement."""
    print("---------should_continue_precision---------")
    print("precision loop count: ", state['precision_loop_count'])
    if state['precision_score'] >= 0.5:  # Threshold for precision
        return "pass"  # Complete the workflow
    else:
        if state['precision_loop_count'] >= state['loop_max_iter']:  # Maximum allowed loops
            return "max_iterations_reached"
        else:
            print(f"---------Precision Score Threshold Not met. Refining Query-----------")  # Debugging
            return "refine_query" # Refine the query
