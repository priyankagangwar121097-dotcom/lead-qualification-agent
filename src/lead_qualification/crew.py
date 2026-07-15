from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class LeadQualification:
    """Lead Qualification crew"""

    @agent
    def lead_qualification_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_qualification_agent"],
            llm=LLM(
                model="groq/llama-3.3-70b-versatile"
            ),
            verbose=True
        )

    @task
    def qualify_lead_task(self) -> Task:
        return Task(
            config=self.tasks_config["qualify_lead_task"]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.lead_qualification_agent()],
            tasks=[self.qualify_lead_task()],
            process=Process.sequential,
            verbose=True
        )