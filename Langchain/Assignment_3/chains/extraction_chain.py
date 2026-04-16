from prompts.extraction_prompt import extraction_prompt
from utils.config import get_llm

# Initialize LLM
llm = get_llm()

# Create chain using LCEL
extraction_chain = extraction_prompt | llm