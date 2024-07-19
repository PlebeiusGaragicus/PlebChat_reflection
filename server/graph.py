from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    MODEL = "phi3:latest"
    llm = ChatOllama(model=MODEL,
                     keep_alive="-1" # Keep the model alive indefinitely
        )


    return {"messages": [llm.invoke(state["messages"])]}



graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

GRAPH_ASCII = graph.get_graph().draw_ascii()
print(GRAPH_ASCII)
