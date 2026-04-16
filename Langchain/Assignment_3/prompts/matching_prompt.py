from langchain_core.prompts import PromptTemplate

matching_prompt = PromptTemplate(
    input_variables=["extracted_resume", "job_description"],
    template="""
You are an expert resume-job matching system.

You are given:
1. Extracted resume data (in JSON format)
2. Job description (text)

Your task:
- Identify required skills and tools from the job description
- Compare them with the candidate's extracted resume data
- Determine matches and missing items

Rules:
- Do NOT assume any skills or tools not present
- Only use the provided data
- Be strict and objective

Evaluate:
- Skills match
- Tools match
- Experience match (Yes/No based on requirement)

Return ONLY a valid JSON object. Do not include any explanation or extra text.

Output Format:
{{
    "matched_skills": [],
    "missing_skills": [],
    "matched_tools": [],
    "missing_tools": [],
    "experience_match": "Yes/No"
}}

Extracted Resume:
{extracted_resume}

Job Description:
{job_description}
"""
)