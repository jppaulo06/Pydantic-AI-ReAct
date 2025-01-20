from loguru import logger
from environs import Env
import httpx
from pydantic_ai import Agent, Tool

env = Env()
env.read_env()

SERPER_API_KEY = env.str("SERPER_API_KEY")
serper_client = httpx.Client(headers={"X-API-KEY": SERPER_API_KEY})


def search(thought: str, query: str):
    """
    Search for a query on Google

    Args:
        thought (str): Your thought about what to do next
        query (str): The query to search for

    Returns:
        str: The search results
    """

    logger.info(f"Thought: {thought}")
    logger.info(f"Searching for: {query}")

    serper_google_url = "https://google.serper.dev/search"
    payload = {"q": query}

    try:
        response = serper_client.post(serper_google_url, json=payload)
        return f"Observation: {response.text}"
    except Exception:
        logger.error("Error searching for the query")
        return "Observation: There was an error while searching for the query"


def access_url(thought: str, url: str):
    """
    Access a URL and scrape the content

    Args:
        thought (str): Your thought about what to do next
        url (str): The URL to access

    Returns:
        str: The scraped content
    """

    logger.info(f"Thought: {thought}")
    logger.info(f"Accessing URL: {url}")

    serper_scraper_url = "https://scrape.serper.dev"
    payload = {"url": url}

    try:
        response = serper_client.post(serper_scraper_url, json=payload)
        return f"Observation: {response.text}"
    except Exception:
        logger.error("Error accessing the URL")
        return "Observation: There was an error while accessing the URL"


system_prompt = """
You are a ReAct (Reasoning and Acting) agent tasked with answering the following query:

Your goal is to reason about the query and decide on the best course of action to answer it accurately.

Instructions:
1. Analyze the query, previous reasoning steps, and observations.
2. Decide on the next action: think about what to do next, use the correct tool, or provide a final answer.
3. Always think before acting.

Remember:
- Be thorough in your reasoning.
- Use tools when you need more information.
- Always base your reasoning on the actual observations from tool use.
- If a tool returns no results or fails, acknowledge this and consider using a different tool or approach.
- Provide a final answer only when you're confident you have sufficient information.
- If you cannot find the necessary information after using available tools, admit that you don't have enough information to answer the query confidently.

Example:

Query: What is the capital of France, and how many people live there?

Thought: I need to find the capital of France, and then I can search for the population of the city.
Search: Capital of France
Observation: The capital of France is Paris.

Thought: Now that I know the capital, I can search for the population of Paris.
Search: Population of Paris
Observation: The population of Paris is approximately 2.1 million.

Thought: I have all the information needed to answer the query.
Final Answer: The capital of France is Paris, and approximately 2.1 million people live there.
"""


agent = Agent(
    model="openai:gpt-4o",
    result_type=str,
    tools=[
        Tool(search, takes_ctx=False),
        Tool(access_url, takes_ctx=False),
    ],
    system_prompt=system_prompt,
)

result = agent.run_sync(
    "What is Apple’s best performing product line from the financial perspective? And what are they marketing on their website?"
)

logger.info(result.data)
