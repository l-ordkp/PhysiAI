def router_decision(state):
    print("---------Routing Decision---------")
    intent = state.get("intent", "")
    if intent == "send_email":
        return "send_email"
    elif intent == "summarise_unread_email":
        return "summarise_unread_emails"
    else:
        return "end"
