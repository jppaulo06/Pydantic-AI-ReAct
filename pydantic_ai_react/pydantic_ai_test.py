from pydantic_ai import Agent
from loguru import logger
from pydantic_ai_react.pydantic_ai_react import react_tool
from lib.tools import search_impl, access_url_impl
from lib.env import load_env
from lib.prompts import USER_QUESTION, PYDANTIC_REACT_SYSTEM_PROMPT


def log_formated_thought(thought: str) -> None:
    logger.info(f"Thought: {thought}")


agent = Agent(
    model="openai:gpt-4o",
    result_type=str,
    system_prompt=PYDANTIC_REACT_SYSTEM_PROMPT,
)


@agent.tool_plain
@react_tool(log_formated_thought)
def search(query: str) -> str:
    """
    Search for a query on Google

    Args:
        query (str): The query to search for

    Returns:
        str: The search results
    """
    return search_impl(query)


@agent.tool_plain
@react_tool(log_formated_thought)
def access_url(url: str) -> str:
    """
    Access a URL and scrape the content

    Args:
        url (str): The URL to access

    Returns:
        str: The scraped content
    """
    return access_url_impl(url)


def main():
    load_env()
    result = agent.run_sync(USER_QUESTION)
    logger.info(result.data)


if __name__ == "__main__":
    main()
