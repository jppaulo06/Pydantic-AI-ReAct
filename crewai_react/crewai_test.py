from crewai import Agent, Crew, Task
from crewai.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field
from lib.tools import search_impl, access_url_impl
from lib.env import load_env
from crewai.agents.parser import AgentAction, AgentFinish


class SearchToolInput(BaseModel):
    query: str = Field(..., description="The search query")


class SearchTool(BaseTool):
    name: str = "Search"
    description: str = "Search for a query and return the search results"

    def _run(self, query: str):
        return search_impl(query)


class AccessUrlToolInput(BaseModel):
    url: str = Field(..., description="The URL to access")


class AccessUrlTool(BaseTool):
    name: str = "Access URL"
    description: str = "Access a URL and return the HTML content"

    def _run(self, url: str):
        return access_url_impl(url)


def step_callback(step):
    if isinstance(step, AgentAction):
        # get until Action Input line
        action_lines = []
        for line in step.text.split("\n"):
            if "Action Input" == line[:12]:
                action_lines.append(line)
                break
            action_lines.append(line)
        logger.info("\n".join(action_lines))
    elif isinstance(step, AgentFinish):
        logger.info(f"Finish: {step.text}")


def main():
    load_env()

    agent = Agent(
        role="Search Agent",
        backstory="You are a focused and determined search agent, which is always ready to find the information asked",
        goal="To answer questions made by the user.",
        tools=[SearchTool(), AccessUrlTool()],
        llm="gpt-4o",
    )

    task = Task(
        name="User Question",
        description="What is Apple’s best performing product line from the financial perspective? And what are they marketing on their website?",
        expected_output="What is Apple’s best performing product line from the financial perspective? And what are they marketing on their website?",
        agent=agent,
    )

    crew = Crew(
        name="React Crew", agents=[agent], tasks=[task], step_callback=step_callback
    )
    respose = crew.kickoff()
    logger.info(respose)


if __name__ == "__main__":
    main()
