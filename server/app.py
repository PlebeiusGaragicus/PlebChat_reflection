import dotenv
dotenv.load_dotenv()

from typing import List
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

# PORT = 8513
app = FastAPI()




class PostRequest(BaseModel):
    user_message: str
    messages: List[dict]
    body: dict


from server.graph.graph import graph
from server.common.commands import handle_commands
from server.common.payment import assure_positive_balance


@app.post("/template")
async def main(request: PostRequest):

    query = request.user_message
    # if query.startswith("/"):
    #     return StreamingResponse(handle_commands(request), media_type="text/event-stream")


    

    # CALCULATE TOKENS FOR INPUT
    # NOTE: maybe we should just do this in the graph nodes.... because we don't yet know how long the input prompt to any given LLM will be
    # ... it may be best practice to just rely on node logic to handle balance deductions

    def call_command():
        # yield from handle_commands(request)
        return handle_commands(request)


    async def event_stream():
        graph_input = {
                "messages": [request.messages[-1]],
                "lud16": request.body['user']['email']
            }

        config = {"configurable": {
            "lud16": request.body['user']['email']
        }}

        async for event in graph.astream_events(input=graph_input, config=config, version="v2"):
            kind = event["event"]
            if  kind == "on_chat_model_stream" or kind=="on_chain_stream":
                content = event["data"]["chunk"]

                if content:
                    if isinstance(content, dict):
                        yield ''
                        # pass
                    else:
                        print(content.content, end="")
                        yield content.content

    if query.startswith("/"):
        return StreamingResponse(call_command(), media_type="text/event-stream")
    # CHECK BALANCE
    elif not assure_positive_balance(request.body['user']['email']):
        # yield "Insufficient balance. Please top up your account."
        return StreamingResponse(iter(["Insufficient balance. Please top up your account."]), media_type="text/event-stream")
    else:
        return StreamingResponse(event_stream(), media_type="text/event-stream")



# if __name__ == "__main__":
#     # TODO: LangSmith setup!

#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=PORT)
