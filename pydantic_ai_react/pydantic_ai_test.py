from environs import Env
import httpx
from pydantic_ai import Agent
from loguru import logger
from pydantic_ai_react.pydantic_ai_react import react_tool, REACT_BASE_PROMPT


def log_formated_thought(thought: str):
    logger.info(f"Thought: {thought}")


env = Env()
env.read_env()
SERPER_API_KEY = env.str("SERPER_API_KEY")
serper_client = httpx.Client(headers={"X-API-KEY": SERPER_API_KEY})

agent = Agent(
    model="openai:gpt-4o",
    result_type=str,
    system_prompt=REACT_BASE_PROMPT,
)


@agent.tool_plain
@react_tool(log_formated_thought)
def search(query: str):
    """
    Search for a query on Google

    Args:
        query (str): The query to search for

    Returns:
        str: The search results
    """

    logger.info(f"Searching for: {query}")

    serper_google_url = "https://google.serper.dev/search"
    payload = {"q": query}

    try:
        response = serper_client.post(serper_google_url, json=payload)
        return f"{response.text}"
    except Exception:
        logger.error("Error searching for the query")
        return "There was an error while searching for the query"


@agent.tool_plain
@react_tool(log_formated_thought)
def access_url(url: str):
    """
    Access a URL and scrape the content

    Args:
        url (str): The URL to access

    Returns:
        str: The scraped content
    """

    logger.info(f"Accessing URL: {url}")

    serper_scraper_url = "https://scrape.serper.dev"
    payload = {"url": url}

    try:
        response = serper_client.post(serper_scraper_url, json=payload)
        return f"{response.text}"
    except Exception:
        logger.error("Error accessing the URL")
        return "There was an error while accessing the URL"


result = agent.run_sync(
    "What is Apple’s best performing product line from the financial perspective? And what are they marketing on their website?"
)

logger.info(result.data)
