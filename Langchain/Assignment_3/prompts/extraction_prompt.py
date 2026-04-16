from langchain_core.prompts import PromptTemplate

extraction_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
You are an expert resume information extractor.

Extract information ONLY from the given resume.
Do NOT assume or infer any information.
If a field is not present, return:
- "Not mentioned" for text fields
- [] for list fields

Extract the following:
- job_title
- skills
- experience (in format: "X years" or "X months")
- tools

Return ONLY a valid JSON object. Do not include any explanation or extra text.

Expected Output Format:
{{
    "job_title": "string",
    "skills": [],
    "experience": "string",
    "tools": []
}}

Resume:
{resume}
"""
)