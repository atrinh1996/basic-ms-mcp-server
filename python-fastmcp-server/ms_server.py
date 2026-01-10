import config
from tools.call import user_info_handler, mail_read_handler, mail_send_handler
from mcp.server.fastmcp import FastMCP

# create an FastMCP server
mcp = FastMCP("teams-mcp-server")


# Tool handlers defined with FastMCP decorator
@mcp.tool()
async def user_info() -> str:
    return await user_info_handler()

@mcp.tool()
async def mail_read(label_id: str) -> str:
    return await mail_read_handler(label_id)

@mcp.tool()
async def mail_send(subject: str, content: str, recipients: list[str]) -> str:
    return await mail_send_handler(subject, content, recipients)


# run server as standalone
if __name__ == "__main__":
    if not config.CLIENT_ID:
        raise Exception("Error: TEAMS_CLIENT_ID environment variable not set")
    # start mcp server
    mcp.run()