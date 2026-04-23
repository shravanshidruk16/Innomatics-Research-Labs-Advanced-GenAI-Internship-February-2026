from langgraph.graph import StateGraph

from typing import TypedDict

class GraphState(TypedDict, total=False):
    query: str
    answer: str
    retriever: object
    llm: object    


def process_node(state: GraphState):
    query = state["query"]
    retriever = state["retriever"]
    llm = state["llm"]

    docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are a customer support assistant for NovaTech.

    Answer ONLY using the provided context.
    If the answer is not in context, say "I don't know".

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)

    return {
        "query": query,
        "answer": response.content,
        "retriever": retriever,
        "llm": llm
    }


def output_node(state):
    return state


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("process", process_node)
    graph.add_node("decision", decision_node)
    graph.add_node("respond", output_node)
    graph.add_node("escalate", escalation_node)

    graph.set_entry_point("process")

    graph.add_edge("process", "decision")

    # Conditional routing
    graph.add_conditional_edges(
        "decision",
        lambda state: state["decision"],
        {
            "respond": "respond",
            "escalate": "escalate"
        }
    )

    return graph.compile()

def decision_node(state):
    from routing.router import route_decision
    
    decision = route_decision(state)
    return {"decision": decision}

from hitl.escalation import human_intervention
def escalation_node(state):
    query = state["query"]
    
    human_response = human_intervention(query)

    return {
        "query": query,
        "answer": human_response,
        "retriever": state["retriever"],
        "llm": state["llm"]
    }