from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama
from langchain_core.chat_history import AIMessage, BaseMessage

from server.common.balance_manager import BalanceManager, deduct
from server.graph import State



def chatbot(state: State, config: RunnableConfig):
    # bm = BalanceManager()

    # lud16 = config["configurable"].get("lud16")
    # if not lud16:
    #     raise ValueError("User's lud16 is not specified")
    # bm.deduct_balance(lud16, "chat_12345", 1.0)


    MODEL = "phi3:latest"
    llm = ChatOllama(model=MODEL,
                     keep_alive="-1" # Keep the model alive indefinitely
        )

    r = llm.invoke(state["messages"])

    # r = BaseMessage(
    #     content="hji",
    #     type="assistant"
    # )

    #TODO: calculate usage
    deduct(config["configurable"].get("lud16"), "chat_12345", 1.0)
    return {"messages": [r]}

    # resp = {
    #     "role": "assistant",
    #     "content": "hi"
    # }

    # return {"messages": [resp]}
    # return {"messages": [AIMessage("hi")]}
    # return {"messages": [{
    #                 "role": "assistant",
    #                 "content": "hi"
    #         }]}
