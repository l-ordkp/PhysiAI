def should_continue_groundedness(state):
  """Decides if groundedness is sufficient or needs improvement."""
  print("---------should_continue_groundedness---------")
  print("groundedness loop count: ", state['groundedness_loop_count'])
  if state['groundedness_score'] >= 0.5:  # Complete the code to define the threshold for groundedness
      print("Moving to precision")
      return "check_precision"
  else:
      if state["groundedness_loop_count"] > state['loop_max_iter']:
        return "max_iterations_reached"
      else:
        print(f"---------Groundedness Score Threshold Not met. Refining Query-----------")
        return "refine_query"