def human_intervention(query):
    print("\n Escalation Triggered!")
    print(f"User Query: {query}")
    
    human_response = input("Enter human response: ")
    
    return human_response