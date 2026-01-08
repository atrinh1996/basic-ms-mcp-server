from mcp.types import Tool
from config import Tools as tool

# handle listing the tools
async def list_tools_handler() -> list[Tool]:
    return [
        Tool(
            name=tool.user_info,
            description="Returns information about user",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name=tool.mail_read,
            description="Read mail",
            inputSchema={
                "type": "object",
                "properties": {
                    "label_id": { "type": "string", "description": "The ID of the mailbox to read from" },
                },
                "required": []
            }
        ),
        Tool(
            name=tool.mail_send,
            description="Send an Email",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject": { "type": "string", "description": "Email Subject" },
                    "content": { "type": "string", "description": "Email Body" },
                    "recipients": { 
                        "type": "array", 
                        "description": "List of emails to send message to",
                        "minItems": 1,
                        "uniqueItems": True,
                        "items": { "type": "string", "format": "email" }
                    },
                },
                "required": ["subject", "content", "recipients"]
            }
        ),



        # Tool(
        #     name=tool.list_teams,
        #     description="List all Teams you're a member of",
        #     inputSchema={
        #         "type": "object",
        #         "properties": {},
        #         "required": []
        #     }
        # ),
        # Tool(
        #     name=tool.list_channels,
        #     description="List channels in a specific team",
        #     inputSchema={
        #         "type": "object",
        #         "properties": {
        #             "team_id": {
        #                 "type": "string",
        #                 "description": "The ID of the team"
        #             }
        #         },
        #         "required": ["team_id"]
        #     }
        # ),
        # Tool(
        #     name=tool.send_message,
        #     description="Send a message to a Teams channel",
        #     inputSchema={
        #         "type": "object",
        #         "properties": {
        #             "team_id": { "type": "string", "description": "The ID of the team" },
        #             "channel_id": { "type": "string", "description": "The ID of the channel" },
        #             "message": { "type": "string", "description": "The message to send" },
        #         },
        #         "required": ["team_id", "channel_id", "message"]
        #     }
        # ),
    ]