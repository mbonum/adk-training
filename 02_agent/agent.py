import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.genai import types
from google.adk.tools import google_search


load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")


async def main():
    root_agent = LlmAgent(
        model="gemini-2.5-flash",
        name="root_agent",
        description="A helpful assistant for user questions.",
        instruction="I can answer your questions by searching the internet. Just ask me anything!",
        tools=[google_search],
    )

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="user_1"
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
