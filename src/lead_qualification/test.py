from crewai import LLM

llm = LLM(
    model="groq/llama-3.3-70b-versatile"
)

response = llm.call("Say hello")

print(response)