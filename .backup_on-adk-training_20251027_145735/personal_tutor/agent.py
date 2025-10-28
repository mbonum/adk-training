from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext
from typing import Dict, Any


def set_user_preferences(
    language: str, difficulty_level: str, tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Set user learning preferences that should be stored persistently
    across all sessions for the current user.
    """
    # TODO: Store the language and difficulty_level in the tool_context.state.
    # Use the correct prefix for data that should persist for the user.
    print(f"TODO: Set user preferences: {language}, {difficulty_level}")

    tool_context.state["user:language"] = language
    tool_context.state["user:difficulty_level"] = difficulty_level

    return {"status": "success", "message": "Preferences saved!"}


def start_learning_session(topic: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Start a new learning session. The current topic should only be
    remembered for the duration of the current conversation session.
    """
    # TODO: Store the topic in the tool_context.state.
    # Use the correct prefix for data that should only last for one session.
    print(f"TODO: Start session on topic: {topic}")

    tool_context.state["session:topic"] = topic

    return {"status": "success", "message": f"Started learning session: {topic}"}


def calculate_quiz_grade(
    correct_answers: int, total_questions: int, tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Calculate a quiz grade. The raw percentage should be stored, but only
    for the current turn. It should be discarded immediately after this
    tool finishes.
    """
    percentage = (correct_answers / total_questions) * 100
    # TODO: Store the 'percentage' in the tool_context.state.
    # Use the correct prefix for data that is temporary for one turn.
    print(f"TODO: Calculate quiz grade. Percentage: {percentage}")

    tool_context.state["temp:quiz_percentage"] = percentage

    return {"status": "success", "percentage": round(percentage, 1)}


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Personal learning tutor that tracks your progress, preferences, and learning history.",
    instruction="""
    You are a personalized learning tutor (Course Version {app:course_version?}) with memory of the user's progress.

    CAPABILITIES:
    - Set and remember user preferences (language, difficulty level)
    - Track completed topics and quiz scores across sessions
    - Start new learning sessions on specific topics
    - Calculate quiz grades and store results
    - Search past learning sessions for context
    - Adapt teaching based on user's level and history

    WORKFLOW:
    1. If new user, ask about preferences (language, difficulty).
    2. For learning requests, start a session with start_learning_session and teach the topic.
    3. After teaching, record completion with the user's quiz score.
    4. When asked, search past lessons to provide context.

    Always be encouraging and adapt to the user's learning pace!
    """,
    tools=[
        set_user_preferences,
        start_learning_session,
        calculate_quiz_grade,
        # record_topic_completion,
        # get_user_progress,
        # search_past_lessons
    ],
    output_key="last_tutor_response",
)
