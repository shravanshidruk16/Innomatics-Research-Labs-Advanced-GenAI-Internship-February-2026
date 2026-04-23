def route_decision(state):
    query = state["query"].lower()
    answer = state["answer"].lower()

    # escalation cases from PDF
    if "refund" in query:
        return "escalate"
    
    if "payment issue" in query:
        return "escalate"

    if "not found" in answer or len(answer) < 30:
        return "escalate"

    return "respond"