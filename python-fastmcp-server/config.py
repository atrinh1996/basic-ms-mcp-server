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
    "User.Read",
    "Mail.Read",
    "Mail.Send",
]

# important endpoints
class Endpoints:
    me = "/me"
    mailReadAll = "/me/messages"

    @staticmethod
    def mailReadByID(id): return f"/me/mailFolders/{id}/messages"

    mailSend = "/me/sendMail"