import asyncio

from agent import agent
from langgraph.types import Command

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