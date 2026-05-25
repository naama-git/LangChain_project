# agent
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from netfree_unstrict_ssl import unstrict_ssl
unstrict_ssl()

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

from langchain.agents.middleware import HumanInTheLoopMiddleware 
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langchain_core.tools import tool

model= ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL_NAME"), google_api_key=os.getenv("GEMINI_API_KEY"))

tavily_key=os.getenv("TAVILY_API_KEY")
tavily_tool = TavilySearch(max_results=5, topic="general")
from prompts import AGENT_SYSTEM_PROMPT


@tool
def ask_user(question: str, sources: list[dict]) -> str:
    """
    Ask the user which sources to include in the summary.
    Each source has 'title' and 'url'. The user can reply in any format:
    indexes ('1 2 3'), natural language ('I want sources 1 and 3'),
    or URLs ('use https://...'). Pass the raw reply to the agent as-is.
    """
    return ""


agent = create_agent(
    model=model,
    system_prompt=AGENT_SYSTEM_PROMPT,
    tools=[tavily_tool, ask_user],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "ask_user": {"allowed_decisions": ["respond"]},
            }
        )    ],
    checkpointer=InMemorySaver(),
)


