def router_decision(state):
    print("---------Routing Decision---------")
    intent = state.get("intent", "")
    if intent == "email":
        return "email"
    elif intent == "calendar":
        return "calendar"
    elif intent == "rag":
        return "rag"
    else:
        return "other"
