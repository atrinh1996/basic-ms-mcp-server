import config, httpx
from pathlib import Path
from utils.ms_auth import MSAuth

# init authorization helper
auth = MSAuth(
    config.CLIENT_ID, 
    config.TENANT_ID, 
    config.TOKEN_CACHE_FILE
)


async def call_graph_api(
    token_cache_file: Path, 
    scopes: list,
    endpoint: str,
    method: str = "GET",
    data: dict = None
):
    """Make a call to Microsoft Graph API"""
    token = await auth.get_token(token_cache_file, scopes)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = f"{config.GRAPH_API_BASE}{endpoint}"

    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(url=url, headers=headers)
        elif method == "POST":
            response = await client.post(url=url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()

        if response.status_code == 204 or response.status_code == 202 or not response.content:
            return None
        return response.json()