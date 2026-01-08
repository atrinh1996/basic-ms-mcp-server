import asyncio, json, os, msal, httpx
from pathlib import Path 
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import config
from tools.list import list_tools_handler
from tools.call import call_tool_handler

# from mcp.server import Server
# from mcp.server.fastmcp import FastMCP

# create an MCP server
app = Server("teams-mcp-server")
# mcp = FastMCP("teams-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return await list_tools_handler()

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    return await call_tool_handler(name, arguments)

async def main():
    if not config.CLIENT_ID:
        raise Exception("Error: TEAMS_CLIENT_ID environment variable not set")

    # start MCP server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

# run server as standalone
if __name__ == "__main__":
    asyncio.run(main())