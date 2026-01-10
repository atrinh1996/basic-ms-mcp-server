import config
from mcp.types import TextContent
from config import Tools as tool
from config import Endpoints as endpoint
from tools.call_graph_api import call_graph_api

# handles calling the tools
async def call_tool_handler(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == tool.user_info:
            # REFERENCE: https://learn.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0&tabs=http
            me = await call_graph_api(
                token_cache_file=config.TOKEN_CACHE_FILE,
                scopes=config.SCOPES,
                endpoint=endpoint.me,
            )
            if not me:
                return [TextContent(type="text", text="No profile found.")]
            
            result = f"\tID: {me['id']}\n"
            result += f"\tName: {me['displayName']}\n"
            result += f"\tMail: {me['mail']}\n"
            result += f"\tPrincipal Name: {me['userPrincipalName']}\n"

            return [TextContent(type="text", text=result)]

        elif name == tool.mail_read:
            label_id = arguments.get("label_id", None)
            # REFERENCE: https://learn.microsoft.com/en-us/graph/api/user-list-messages?view=graph-rest-1.0&tabs=http
            # REFERENCE: https://learn.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0
            data = await call_graph_api(
                token_cache_file=config.TOKEN_CACHE_FILE,
                scopes=config.SCOPES,
                endpoint=endpoint.mailReadByID(label_id) if label_id else endpoint.mailReadAll,
            )
            mail = data.get("value", [])
            if not mail:
                return [TextContent(type="text", text="No Mail found.")]
            
            # import json
            # result = str(json.dumps(mail[0], indent=4))
            result = "Your Messages:"
            for message in mail:
                result += "\n\n"
                result += f"\tSubject: {message.get('subject', '')}\n"
                # use 'sender' or 'from'
                sender_name = message['sender']['emailAddress']['name']
                sender_email = message['sender']['emailAddress']['address']
                result += f"\tSender: {sender_name}\n"
                result += f"\tSender Email: {sender_email}\n"
                # result += f"\tContent: {message['body']['content']}\n\n"
                result += f"\tContent Preview: {message['bodyPreview']}\n\n"
                result += "*" * 30

            return [TextContent(type="text", text=result)]
        
        elif name == tool.mail_send:
            # REFERENCE: https://learn.microsoft.com/en-us/graph/api/user-sendmail?view=graph-rest-1.0&tabs=http
            subject = arguments["subject"]
            content = arguments["content"]
            recipients = arguments["recipients"] # list of email addresses 

            toRecipients: list = [{"emailAddress": {"address": email}} for email in recipients]

            message = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "Text",
                        "content": content
                    },
                    "toRecipients": toRecipients,
                },
                "saveToSentItems": "false"
            }

            await call_graph_api(
                token_cache_file=config.TOKEN_CACHE_FILE,
                scopes=config.SCOPES,
                endpoint=endpoint.mailSend,
                method="POST",
                data=message
            )
            return [TextContent(type="text", text=f"Email '{subject}' sent.")]




        # elif name == tool.list_teams:
        #     data = await call_graph_api(
        #         token_cache_file=config.TOKEN_CACHE_FILE,
        #         scopes=config.SCOPES,
        #         endpoint=endpoint.joinedTeams,
        #     )
        #     teams = data.get("value", [])

        #     if not teams:
        #         return [TextContent(type="text", text="No teams found.")]
            
        #     result = "Your teams:\n\n" + "\n".join([f"\t{team['displayName']} (ID: {team['id']})" for team in teams])
        #     return [TextContent(type="text", text=result)]
        
        # elif name == tool.list_channels:
        #     team_id = arguments["team_id"]
        #     data = await call_graph_api(
        #         token_cache_file=config.TOKEN_CACHE_FILE,
        #         scopes=config.SCOPES,
        #         endpoint=endpoint.teamsChannels(team_id),
        #     )
        #     channels = data.get("value", [])

        #     if not teams:
        #         return [TextContent(type="text", text="No channels found.")]

        #     result = "Your channels:\n\n" + "\n".join([f"\t{channel['displayName']} (ID: {channel['id']})" for channel in channels])
        #     return [TextContent(type="text", text=result)]
        
        # elif name == tool.send_message:
        #     team_id = arguments["team_id"]
        #     channel_id = arguments["channel_id"]
        #     message = arguments["message"]

        #     message_data = { "body": { "content": message } }

        #     await call_graph_api(
        #         token_cache_file=config.TOKEN_CACHE_FILE,
        #         scopes=config.SCOPES,
        #         endpoint=endpoint.channelMessages(team_id, channel_id),
        #         method="POST",
        #         data=message_data
        #     )
        #     return [TextContent(type="text", text="Message sent.")]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]