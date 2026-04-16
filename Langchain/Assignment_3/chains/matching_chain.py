from prompts.matching_prompt import matching_prompt
from utils.config import get_llm

# Initialize LLM
llm = get_llm()

# Create chain using LCEL
matching_chain = matching_prompt | llm