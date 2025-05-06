def router_decision(state):
    print("---------Routing Decision---------")
    intent = state.get("intent", "")
    if intent == "create":
        return "create_event"
    elif intent in ["update", "delete","list"]:
        return "list_of_events"
    else:
        return "end"
