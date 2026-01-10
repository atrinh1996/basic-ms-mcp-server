import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configurations
CLIENT_ID = os.getenv("TEAMS_CLIENT_ID")
CLIENT_SECRET = os.getenv("TEAMS_CLIENT_SECRET")
# TENANT_ID = "common" # personal accounts (might be failing)
TENANT_ID = "consumers" # personal MS acocunts
TOKEN_CACHE_FILE = Path.home()/".ms_mcp_token_cache.json"

# print(CLIENT_ID)
# print(TOKEN_CACHE_FILE)

# MS Graph API endpoint
GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"

# API Permissions/Scopes
SCOPES = [
    # "Channel.ReadBasic.All",
    # "Chat.ReadWrite",
    # "Team.ReadBasic.All",
    "User.Read",
    # "User.ReadBasic.All",
    "Mail.Read",
    "Mail.Send",
    # "Team.ReadBasic.All",
]

# list of tools for Teams MCP
class Tools:
    # Forbidden with personal only accounts
    # list_teams = "list_teams"
    # list_channels = "list_channels"
    # send_message = "send_message"

    user_info = "user_info"
    mail_read = "mail_read"
    mail_send = "mail_send"

# important endpoints
class Endpoints:
    me = "/me"
    mailReadAll = "/me/messages"

    @staticmethod
    def mailReadByID(id): return f"/me/mailFolders/{id}/messages"

    mailSend = "/me/sendMail"

    # work or school accounts only
    # joinedTeams = "/me/joinedTeams" # list of Teams user is in
    # def teamsChannels(team_id): return f"/teams/{team_id}/channels"
    # def channelMessages(team_id, channel_id): return f"/teams/{team_id}/channels/{channel_id}/messages"