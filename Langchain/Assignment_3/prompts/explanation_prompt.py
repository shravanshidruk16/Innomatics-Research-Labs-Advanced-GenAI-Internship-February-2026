from langchain_core.prompts import PromptTemplate

explanation_prompt = PromptTemplate(
    input_variables=["matching_data", "match_score"],
    template="""
You are an expert AI recruiter assistant.

You are given:
1. Matching data between resume and job description (JSON)
2. Final match score (0-100)

Your task:
Provide a clear and concise explanation of why this score was assigned.

Rules:
- Base your explanation ONLY on the provided data
- Do NOT assume any information
- Be objective and factual
- Highlight:
    - Matched skills
    - Missing skills
    - Tools match
    - Experience match

Return a short explanation (3-5 lines).

Output Format:
{{
    "explanation": "your explanation here"
}}

Matching Data:
{matching_data}

Match Score:
{match_score}
"""
)