from prompts.explanation_prompt import explanation_prompt
from utils.config import get_llm

# Initialize LLM
llm = get_llm()

# Create chain using LCEL
explanation_chain = explanation_prompt | llm