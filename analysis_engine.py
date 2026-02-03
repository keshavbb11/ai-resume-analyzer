from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

llm = Ollama(model="llama3")

analysis_prompt = ChatPromptTemplate.from_template("""
You are an unbiased technical recruiter.

Use ONLY the resume context below.
Ignore name, age, gender, college, and location.

<context>
{context}
</context>

Job Description:
{job_description}

IMPORTANT RULES:
- Return ONLY valid JSON
- Do NOT include explanations
- Do NOT include markdown
- Do NOT include text before or after JSON

Return EXACTLY this structure:
{{
  "skills_found": [],
  "missing_skills": [],
  "skills_score": 0,
  "experience_score": 0,
  "projects_score": 0,
  "clarity_score": 0
}}
""")

analysis_chain = analysis_prompt | llm