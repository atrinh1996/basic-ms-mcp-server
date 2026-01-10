# About
Basic MCP Server that connects to MS Account. Uses older mcp.server

# Considerations
- Note that successful authentications will cache tokens at ~/.ms_mcp_token_cache.json
- You will use the device code at: https://www.microsoft.com/link

# Requirements
- Activate a virtual environment and install the following python packages
    - `mcp`
    - `msal` (Microsoft Authentication Library)
    - `httpx`

- MS Account
    - Create a Microsoft Account and register an app on portal.azure.com
        - Note that Access to certain Graph API permissions require school/work accounts. If you only have a personal account, configure scope/permission accordingly. 
        - Authentication will likely fail if your account type does not meet the requirements for the scope it is requesting.
    - Create the following under the registered App:
        - Client secret
        - Authenticate via Web and Mobile and Desktop Applications
            - Enable public client flows
            - Web Redirect URI: remove this
            - Mobile and desktop Redirect URI:  https://login.microsoftonline.com/common/oauth2/nativeclient
        - API permissions and grant admin consent:
            - Requires work or school account only (i.e. MS Teams):
                - Channel.ReadBasic.All
                - Chat.ReadWrite
                - Team.ReadBasic.All
            - Allowed for personal accounts:
                - User.Read (user info)
                - Mail.Read (outlook email read)
                - Mail.Send (outlook email write and send)

- Environment Variables (set or put in .env):
    - TEAMS_CLIENT_ID
    - TEAMS_CLIENT_SECRET (not currently used)

- Other tools
    - Install `npm`, `node`, `npx`

# Test Server

```sh
npx @modelcontextprotocol/inspector python ms_server.py
```

# Run Server

```sh
python ms_server.py
```

- Trigger a tool call to trigger authentication