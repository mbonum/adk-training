# import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.agents import SequentialAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

load_dotenv()

GEMINI_MODEL = "gemini-2.5-flash"


async def main():
    code_writer_agent = LlmAgent(
        name="CodeWriterAgent",
        model=GEMINI_MODEL,
        # senior
        instruction="""You are a junior Python Code Generator.
    Based *only* on the user's request, write Python code that satisfies all user's requirements.
    Output *only* the complete Python code block, enclosed in triple backticks (```python ... ```). 
    Do not add any other text before or after the code block.
    """,
        description="Writes initial Python code based on a specification.",
        # Used to access the agent generated code
        output_key="generated_code",  # Stores output in state['generated_code']
    )

    # Take generated_code (read from state) and provide feedback.
    code_reviewer_agent = LlmAgent(
        name="CodeReviewerAgent",
        model=GEMINI_MODEL,
        instruction="""You are an expert Python Code Reviewer. 
        Your task is to provide constructive feedback on the provided code.

        **Code to Review:**
        ```python
        {generated_code}
        ```

    **Review Criteria:**
    1.  **Correctness:** Does the code work as intended? Are there logic errors?
    2.  **Readability:** Is the code clear and easy to understand? Follows PEP 8 style guidelines?
    3.  **Efficiency:** Is the code reasonably efficient? Any obvious performance bottlenecks?
    4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
    5.  **Best Practices:** Does the code follow common Python best practices?

    **Output:**
    Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
    If the code is excellent and requires no changes, simply state: "No major issues found."
    Output *only* the review comments or the "No major issues" statement.
    """,
        description="Reviews code and provides feedback.",
        output_key="review_comments",  # Stores output in state['review_comments']
    )

    # Take generated_code and review_comments (outputs of the previous agents) and refactor the code.
    code_refactorer_agent = LlmAgent(
        name="CodeRefactorerAgent",
        model=GEMINI_MODEL,
        instruction="""You are a senior Python Code Refactoring AI.
    Goal: Improve the given Python code based on the provided review comments.

    **Original Code:**
    ```python
    {generated_code}
    ```

    **Review Comments:**
    {review_comments}

    **Task:**
    Carefully apply the suggestions from the review comments to refactor the original code.
    If the review comments state "No major issues found," return the original code unchanged.
    Ensure the final code is complete, functional, and includes necessary imports and docstrings.

    **Output:**
    Output *only* the final, refactored Python code block, enclosed in triple backticks (```python ... ```). 
    Do not add any other text before or after the code block.
    """,
        description="Refactors code based on review comments.",
        output_key="refactored_code",  # Stores output in state['refactored_code']
    )

    # Orchestrate the pipeline by running the sub_agents in order.
    code_pipeline_agent = SequentialAgent(
        name="CodePipelineAgent",
        # N.B. The order of agents matters: Writer -> Reviewer -> Refactorer
        sub_agents=[code_writer_agent, code_reviewer_agent, code_refactorer_agent],
        description="Executes a sequence of code writing, reviewing, and refactoring.",
    )

    root_agent = code_pipeline_agent

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
