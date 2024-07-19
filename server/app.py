import dotenv
dotenv.load_dotenv()

from typing import List
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
app = FastAPI()

class PostRequest(BaseModel):
    user_message: str
    messages: List[dict]
    body: dict


from graph import graph
from commands import handle_commands


@app.post("/template")
async def main(request: PostRequest):

    query = request.user_message
    if query.startswith("/"):
        return StreamingResponse(handle_commands(request), media_type="text/event-stream")

    i = request.messages[-1]

    async def event_stream():
        # input = request['user_message']
        async for event in graph.astream_events(input={"messages": [i]}, version="v2"):
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

    return StreamingResponse(event_stream(), media_type="text/event-stream")



if __name__ == "__main__":
    # TODO: LangSmith setup!

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8510)
