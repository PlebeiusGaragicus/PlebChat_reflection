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


# body: dict
# {
#     "stream": true,
#     "model": "pipeline_template",
#     "messages": [
#         {
#             "role": "user",
#             "content": "/version"
#         }
#     ],
#     "user": {
#         "name": "local_admin",
#         "id": "b1e31733-d29f-407a-a43a-0de19cfc84a6",
#         "email": "admin@admin.com",
#         "role": "admin"
#     }
# }
# request.body.user.email

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
        from server.graph import GRAPH_ASCII
        return f"```\n{GRAPH_ASCII}\n```"

    elif command == "debug":
        return f"# body:\n```json\n{json.dumps(request.body, indent=4)}\n```"

######################################
# PAYMENT COMMANDS
######################################

    elif command == "bal":
        from .payment import cmd_bal
        return cmd_bal(request)

######################################
# CUSTOM COMMANDS TO THIS AGENT
######################################

    # elif command == "your_custom_command":
    #     yield SOMETHING

######################################
    else:
        return f"Command not found.\n\n```txt\n{USAGE}\n```"
