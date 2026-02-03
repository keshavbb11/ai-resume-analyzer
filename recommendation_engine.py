from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

llm = Ollama(model="llama3")

recommendation_prompt = ChatPromptTemplate.from_template("""
You are a senior career mentor.

<context>
{context}
</context>

Job Description:
{job_description}

Provide:
1. Skill recommendations
2. Project recommendations
3. Resume wording improvements
4. 2-week learning plan
""")

recommendation_chain = recommendation_prompt | llm