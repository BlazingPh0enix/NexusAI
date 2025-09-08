import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from nexus_ai.tools.search_tool import DuckDuckGoSearchTool
from crewai_tools import TavilySearchTool, SerperDevTool
from dotenv import load_dotenv

@CrewBase
class NexusAi():
    """NexusAi crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    load_dotenv()

    ddgs_search_tool = DuckDuckGoSearchTool()

    # # Uncomment and configure if you have Tavily or SerperDev API keys
    # tavily_search_tool = TavilySearchTool(
    #     max_results=10,
    #     api_key=os.getenv("TAVILY_API_KEY", ),
    #     include_answer=True,
    # )

    # serper_search_tool = SerperDevTool()

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            tools=[self.ddgs_search_tool],
            verbose=True
        )
    
    @agent
    def use_case_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['use_case_generator'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def resource_collector(self) -> Agent:
        return Agent(
            config=self.agents_config['resource_collector'], # type: ignore[index]
            tools=[self.ddgs_search_tool],
            verbose=True
        )
    
    @agent
    def feasibility_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['feasibility_analyst'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def proposal_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['proposal_writer'], # type: ignore[index]
            verbose=True
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
            agent=self.researcher()
        )
    
    @task
    def use_case_task(self) -> Task:
        return Task(
            config=self.tasks_config['use_case_task'], # type: ignore[index]
            agent=self.use_case_generator(),
            context=[self.research_task()]
        )
    
    @task
    def resource_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['resource_collection_task'], # type: ignore[index]
            agent=self.resource_collector(),
            context=[self.use_case_task()]
        )
    
    @task
    def feasibility_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['feasibility_analysis_task'], # type: ignore[index]
            agent=self.feasibility_analyst(),
            context=[self.use_case_task()]
        )

    @task
    def proposal_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['proposal_writing_task'], # type: ignore[index]
            agent=self.proposal_writer(),
            context=[self.research_task(), self.use_case_task(), self.resource_collection_task(), self.feasibility_analysis_task()],
            output_file="output/final_proposal.md"
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher(), self.use_case_generator(), self.resource_collector(), self.feasibility_analyst(), self.proposal_writer()],
            tasks=[self.research_task(), self.use_case_task(), self.resource_collection_task(), self.feasibility_analysis_task(), self.proposal_writing_task()],
            process=Process.sequential,
            verbose=True
        )