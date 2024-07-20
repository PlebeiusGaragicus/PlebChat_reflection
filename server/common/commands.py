import json

# Markdown text to explain this construct
CONSTRUCT_INFORMATION = """
# Chatbot Agent

Hi, I'm just some agent dude...

Try `/usage` for a list of commands.
"""


# Markdown text to explain the commands available
USAGE = """
/version                  Get the version of the agent

/info, /about             Get information about the agent

/draw                     Get the graph of the agent

/help, /usage             Get a list of commands

/debug                    Get debug information
"""



def handle_commands(request):
    split = request.user_message.split(" ")
    command = split[0][1:].lower() # Remove the slash and take the first word

######################################
# STANDARD COMMANDS FOR EVERY AGENT
######################################
    if command == "version":
        from server.VERSION import VERSION
        return f"Version `{VERSION}`"

    elif command == "info" or command == "about":
        return CONSTRUCT_INFORMATION

    elif command == "usage" or command == "help":
        return f"```\n{USAGE}\n```"

    elif command == "draw":
        from server.graph.graph import GRAPH_ASCII
        return f"```\n{GRAPH_ASCII}\n```"

    elif command == "debug":
        return f"# body:\n```json\n{json.dumps(request.body, indent=4)}\n```"

######################################
# PAYMENT COMMANDS
######################################

    elif command == "bal":
        from .payment import cmd_bal
        return cmd_bal(lud16=request.body['user']['email'])

######################################
# CUSTOM COMMANDS TO THIS AGENT
######################################

    # elif command == "your_custom_command":
    #     yield SOMETHING

######################################
    else:
        return f"Command not found.\n\n```txt\n{USAGE}\n```"
