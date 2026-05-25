import gradio as gr
from langgraph.types import Command
from agent import agent

css = """
#container {
    max-width: 900px;
    margin: auto;
}
"""

sessions = {}

THREAD_ID = "single_session"


async def chat(message, history):

    config = {
        "configurable": {
            "thread_id": THREAD_ID
        }
    }

    session = sessions.get(THREAD_ID)

    # a new conversation

    if not session:

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            },
            config=config,
            version="v2",
        )


    else:

        interrupt = session["interrupt"]

        decisions = [
            {
                "type": "respond",
                "message": message
            }
        ]

        result = await agent.ainvoke(
            Command(
                resume={"decisions": decisions}
            ),
            config=config,
            version="v2"
        )

        sessions.pop(THREAD_ID)


    # interrupt

    if result.interrupts:

        interrupt = result.interrupts[0]
        request = interrupt.value["action_requests"][0]

        args = request["args"]

        sources_text = "\n".join(
            [
                f"{i}. {src['title']} — {src['url']}"
                for i, src in enumerate(args["sources"], 1)
            ]
        )

        sessions[THREAD_ID] = {
            "interrupt": interrupt
        }

        return (
            f"{args['question']}\n\n{sources_text}"
        )
    

    content = result["messages"][-1].content

    if isinstance(content, list):
        text = next(
            block["text"]
            for block in content
            if block.get("type") == "text"
        )
    else:
        text = content

    return text


with gr.Blocks(css=css) as demo:

    with gr.Column(elem_id="container"):

        gr.ChatInterface(
            fn=chat,
            title="Research Agent",
        )


