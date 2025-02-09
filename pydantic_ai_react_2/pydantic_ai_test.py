from loguru import logger
from pydantic import BaseModel
from pydantic_ai import Agent, Tool
from lib.tools import search_impl, access_url_impl


def think(thought: str):
    """
    Think about what to do next. MUST be used before acting.

    Args:
        thought (str): Your thought about what to do next
    """
    logger.info(f"Thought: {thought}")
    return


def search(query: str):
    """
    Search for a query on Google

    Args:
        query (str): The query to search for

    Returns:
        str: The search results
    """
    return search_impl(query)


def access_url(url: str):
    """
    Access a URL and scrape the content

    Args:
        url (str): The URL to access

    Returns:
        str: The scraped content
    """
    return access_url_impl(url)


system_prompt = """
You are a ReAct (Reasoning and Acting) agent tasked with answering the following query:

Your goal is to reason about the query and decide on the best course of action to answer it accurately.

Instructions:
1. Analyze the query, previous reasoning steps, and observations.
2. Decide on the next action: think about what to do next, use the correct tool, or provide a final answer.
3. Always think before acting. Think before every action to ensure you're on the right track.

Remember:
- Be thorough in your reasoning.
- Use tools when you need more information.
- Always base your reasoning on the actual observations from tool use.
- If a tool returns no results or fails, acknowledge this and consider using a different tool or approach.
- Provide a final answer only when you're confident you have sufficient information.
- If you cannot find the necessary information after using available tools, admit that you don't have enough information to answer the query confidently.
"""


class Action(BaseModel):
    name: str
    reason: str
    input: list


class ActionStep(BaseModel):
    thoght: str
    action: str


class FinalAnswer(BaseModel):
    thoght: str
    answer: str


agent = Agent(
    model="openai:gpt-4o",
    result_type=str,
    tools=[
        Tool(think, takes_ctx=False),
        Tool(search, takes_ctx=False),
        Tool(access_url, takes_ctx=False),
    ],
    system_prompt=system_prompt,
)

result = agent.run_sync(
    "What is Apple’s best performing product line from the financial perspective? And what are they marketing on their website?"
)

logger.info(result.data)
