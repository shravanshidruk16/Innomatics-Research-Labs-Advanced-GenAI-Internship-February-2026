from langchain_core.prompts import PromptTemplate

scoring_prompt = PromptTemplate(
    input_variables=["matching_data"],
    template="""
You are an expert resume scoring system.

You are given matching data in JSON format between a resume and a job description.

Your task:
Assign a score from 0 to 100 based strictly on the following rules.

Scoring Rules:
- Skills match contributes 50% of total score
- Tools match contributes 30% of total score
- Experience match contributes 20% of total score

Evaluation method:
- Skills Score = (number of matched_skills / total required skills) * 50
- Tools Score = (number of matched_tools / total required tools) * 30
- Experience Score:
    - If experience_match = "Yes" → 20
    - If experience_match = "No" → 0

Final Score:
- Sum all three scores
- Ensure final score is between 0 and 100

Rules:
- Do NOT assume any missing data
- Only use the provided JSON
- Be strict and objective

Return ONLY a valid JSON object. No explanation.

Output Format:
{{
    "match_score": 0
}}

Matching Data:
{matching_data}
"""
)