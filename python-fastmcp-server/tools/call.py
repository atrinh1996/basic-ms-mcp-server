import config
from mcp.types import TextContent
from config import Endpoints as endpoint
from tools.call_graph_api import call_graph_api


async def user_info_handler() -> str:
    """Get authenticated user's basic info"""
    try:
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

        return result

    except Exception as e:
        return f"Error: {str(e)}"


async def mail_read_handler(label_id: str = None) -> str:
    """
    Get authenticated user's emails
    
    Args:
        label_id: The ID of the mailbox to read from, eg. "Inbox"
    """
    try:
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
        return result

    except Exception as e:
        return f"Error: {str(e)}"


async def mail_send_handler(subject: str, content: str, recipients: list[str]) -> str:
    """
    Send an email for authenticated user
    
    Args:
        subject: Email Subject
        content: Email Body
        recipients: List of emails to send message to
    """
    try:
        # REFERENCE: https://learn.microsoft.com/en-us/graph/api/user-sendmail?view=graph-rest-1.0&tabs=http
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
        return f"Email '{subject}' sent."

    except Exception as e:
        return f"Error: {str(e)}"


    