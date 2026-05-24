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

model= ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL_NAME"), google_api_key=os.getenv("GEMINI_API_KEY"))

tavily_key=os.getenv("TAVILY_API_KEY")
tavily_tool = TavilySearch(max_results=7, topic="general")
from prompts import AGENT_SYSTEM_PROMPT

agent = create_agent(
    model=model,
    system_prompt=AGENT_SYSTEM_PROMPT,
    tools=[tavily_tool],
)


async def query_loop():
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
            }
        )

        last_message = result["messages"][-1]
        print("\nAgent Response:", last_message.content)


if __name__ == "__main__":
    asyncio.run(query_loop())