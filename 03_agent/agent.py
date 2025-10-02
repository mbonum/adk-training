import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.runners import InMemoryRunner
from google.genai import types
# from google.adk.auth import AuthConfig
# from google.adk.tools import google_search

load_dotenv()

TARGET_FOLDER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "mcp_folder",  # C:\Users\CG713LD\Desktop\dev\on-adk-training\03_agent\mcp_folder
)

api_key = os.getenv("GOOGLE_API_KEY")


async def main():
    root_agent = LlmAgent(
        model="gemini-2.5-flash",
        name="filesystem_assistant_agent",
        description="A helpful assistant for user questions.",
        instruction="Help the user manage their files. You can list files, read files, etc.",
        tools=[
            McpToolset(
                connection_params=StdioConnectionParams(
                    # auth_config=AuthConfig(auth_scheme=None),
                    auth_config=None,
                    server_params=StdioServerParameters(
                        command="npx",
                        args=[
                            "-y",  # Argument for npx to auto-confirm install
                            "@modelcontextprotocol/server-filesystem",
                            # IMPORTANT: This MUST be an ABSOLUTE path to a folder the
                            # npx process can access.
                            # Replace with a valid absolute path on your system.
                            # For example: "/Users/youruser/accessible_mcp_files"
                            # or use a dynamically constructed absolute path:
                            os.path.abspath(TARGET_FOLDER_PATH),
                        ],
                    ),
                ),
                # Optional: Filter which tools from the MCP server are exposed
                # tool_filter=['list_directory', 'read_file']
            )
        ],
    )

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="user_2"
    )

    # user_input = "Qual è la capitale dell'Italia?"

    print("Chat iniziata. Scrivi 'bye', 'quit' o 'exit' per terminare.")

    while True:
        user_input = input("Prompt: ")
        if user_input.lower() in ["bye", "quit", "exit"]:
            print("Chat terminata.")
            break

        # Every content is an artifact
        content = types.UserContent(parts=[types.Part(text=user_input)])

        print("Gemini: ", end="", flush=True)

        # LLM loop
        async for event in runner.run_async(
            user_id=session.user_id, session_id=session.id, new_message=content
        ):
            for part in event.content.parts:
                print(part.text, end="", flush=True)
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())
