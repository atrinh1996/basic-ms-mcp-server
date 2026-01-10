# test client for ms mcp server
import asyncio, os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
load_dotenv()


async def main():
    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["ms_server.py"],
        env={
            "TEAMS_CLIENT_ID": os.getenv("TEAMS_CLIENT_ID"),
        }
    )
    print("Connecting to Teams MCP server...")
    
    # Connect to server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            print("Connected to server")
            
            # List tools
            tools = await session.list_tools()
            print("Available tools:")
            tools = tools.tools
            tools = "\n".join(f"\t{tool.name}" for tool in tools)
            print(tools)
            # tools = [tool.name for tool in tools]
            

            # Try listing teams (this will trigger auth)
            # print("\nCalling user_info (watch for device code above)...")
            # result = await session.call_tool("user_info", arguments={})
            
            # print("\nResult:")
            # for content in result.content:
            #     print(content.text)

            while True:
                operation = input("Select a tool, or 'exit' or 'quit' or 'list': ")
                if operation == 'exit' or operation == 'quit': break

                if operation == 'list':
                    print(tools)
                    continue

                arguments = {}

                if operation == 'user_info':
                    result = await session.call_tool("user_info", arguments=arguments)
                elif operation == 'mail_read':
                    arguments['label_id'] = input("Which mailbox or hit Enter for all mail: ").strip()
                    result = await session.call_tool("mail_read", arguments=arguments)

                elif operation == 'mail_send':
                    arguments['subject'] = input("Email subject line: ").strip()
                    arguments['content'] = input("Paste in email body:\n")
                    recipients = input("Recipient emails, comma separated: ").strip()
                    arguments['recipients'] = [recipient.strip() for recipient in recipients.split(",")]

                    result = await session.call_tool("mail_send", arguments=arguments)
                
                else:
                    print("error: unknown operation")
                    continue
                
                print("\nResult:")
                for content in result.content:
                    print(content.text)



            print("Goodbye")

if __name__ == "__main__":
    asyncio.run(main())