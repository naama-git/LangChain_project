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


def handle_interrupt(action_request: dict) -> dict:
    args = action_request["args"]
    for i, src in enumerate(args["sources"], 1):
        print(f"  {i}. {src['title']} — {src['url']}")
    return {"type": "respond", "message": input("\nYour selection: ").strip()}


async def query_loop():

    config = {"configurable": {"thread_id": "single_session"}}

    while True:
        user_query = input("Enter your query (or 'exit' to quit): ")
        if user_query.strip().lower() in ("exit", "quit"):
            break

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_query,
                    }
                ]
            },
            config=config,
            version="v2",
        )

        while result.interrupts:
            decisions = [
                handle_interrupt(req)
                for interrupt in result.interrupts
                for req in interrupt.value["action_requests"]
            ]
            result = await agent.ainvoke(
                Command(resume={"decisions": decisions}),
                config=config,
                version="v2"
            )


            content = result.value['messages'][-1].content
            if isinstance(content, list):
                text = next(block['text'] for block in content if block.get('type') == 'text')
            else:
                text = content

            print(f"\n{text}\n")


if __name__ == "__main__":
    asyncio.run(query_loop())