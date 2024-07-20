from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama

from server.graph.modules.balance_manager import BalanceManager

from server.graph import State








def chatbot(state: State, config: RunnableConfig):
    bm = BalanceManager("http://localhost:5101")

    lud16 = config["configurable"].get("lud16")
    if not lud16:
        raise ValueError("User's lud16 is not specified")

    # print(config.keys())

    # for key in config.keys():
    #     print(key)
    #     print(config[key])
    
    # print(config['configurable']['__pregel_read'])

    bm.deduct_balance(lud16, "chat_12345", 1.0)
    # Check balance
    # try:
        # balance = bm.check_balance(lud16)
        # print("Current balance:", balance)

        # bm.deduct_balance(lud16, "chat_12345", 1.0)
        # print("New balance after deduction:", result)

    # except ValueError as e:
        # print(e)

    MODEL = "phi3:latest"
    llm = ChatOllama(model=MODEL,
                     keep_alive="-1" # Keep the model alive indefinitely
        )

    return {"messages": [llm.invoke(state["messages"])]}
