from prompts.scoring_prompt import scoring_prompt
from utils.config import get_llm

# Initialize LLM
llm = get_llm()

# Create chain using LCEL
scoring_chain = scoring_prompt | llm