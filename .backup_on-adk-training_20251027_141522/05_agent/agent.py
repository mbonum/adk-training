import asyncio
import os
import time
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.genai import types
from google.adk.tools import google_search
from google.adk.events import Event, EventActions
# from google.adk.agents.invocation_context import InvocationContext


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

    runner = InMemoryRunner(
        agent=root_agent
    )  # it creates session_service = InMemorySessionService()
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="user_1",
        state={"user:inv_count": 0},
    )

    #    invocation_context = InvocationContext(
    #     invocation_id="unique-id-for-this-run",
    #     session=session,
    #     user_content=user_message,
    #     agent=my_root_agent, # The starting agent
    #     session_service=session_service,
    #     artifact_service=artifact_service,
    #     memory_service=memory_service,
    #     # ... other necessary fields ...
    # )

    print("Chat started. Type 'bye', 'quit' or 'exit' to exit.")

    while True:
        user_input = input("Prompt: ")
        if user_input.lower() in ["bye", "quit", "exit"]:
            print("Chat ended.")
            break

        # Every content is an artifact
        content = types.UserContent(parts=[types.Part(text=user_input)])

        print("Gemini: ", end="", flush=True)

        current_time = time.time()

        # LLM loop
        async for event in runner.run_async(
            user_id=session.user_id, session_id=session.id, new_message=content
        ):
            for part in event.content.parts:
                print(part.text, end="", flush=True)
            print("\n")

            state_changes = {
                "user:inv_count": session.state.get("user:inv_count", 0)
                + 1,  # Update invocation count
            }

            print(f"{state_changes['user:inv_count']} total invocazions.")

            actions_with_update = EventActions(state_delta=state_changes)

            # Event from an unknown agent: system, event id: 0c442416-d4a9-431c-8cfe-3eb968aca36a
            system_event = Event(
                invocation_id="inv_count_update",
                author="system",  # Or 'agent', 'tool' etc.
                actions=actions_with_update,
                timestamp=current_time,
                # content might be None or represent the action taken
            )

            await runner.session_service.append_event(session, system_event)


if __name__ == "__main__":
    asyncio.run(main())
