import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

agent = Agent(
    role="Lead Qualification Specialist",
    goal="Evaluate leads according to the provided scoring rules.",
    backstory="You are an expert in evaluating and scoring business leads.",
    llm=llm,
    verbose=True,
    cache=False
)

task = Task(
    description="""
    Evaluate this lead:

    Name: Test Lead
    Business Type: Manufacturing
    City: Delhi
    Investment Capacity: 5000000
    Occupation: Founder

    Return only:
    Score: [number]
    Qualification: [HOT LEAD, WARM LEAD, or COLD LEAD]
    """,
    expected_output="A numerical score and lead qualification.",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential,
    verbose=True,
    cache=False
)

result = crew.kickoff()

print("\nFINAL RESULT:")
print(result)