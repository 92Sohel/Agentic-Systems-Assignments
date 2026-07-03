
#from langchain_ollama import ChatOllama

import os

from httpcore import stream
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

#os.environ["GOOGLE_API_KEY"]="YOUR GOOGLE_API_KEY"

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt_template = PromptTemplate.from_template(
    """Explain {topic} to {audience} with these requirements:
- Use {tone} tone
- Give one real-life analogy to explain the concept
- Keep the response within {limit} words"""
)

final_prompt=prompt_template.format(
    topic="SQL Fundamentals",
    audience="advance",
    tone="harsh",
    limit="300",
    #stream=True
)

response = llm.invoke(final_prompt)
print(response)
print(response.content)




