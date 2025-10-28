# In agent.py (Starter Code)

from google.adk.agents import Agent
# from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

# ============================================================================
# ARTIFACT-HANDLING TOOLS
# ============================================================================


async def extract_text(document_name: str, tool_context: ToolContext) -> str:
    """Extracts and cleans text from a document, saving it as an artifact."""
    extracted_content = f"EXTRACTED AND CLEANED TEXT FROM DOCUMENT: {document_name}"

    # TODO: 1. Create a types.Part from the `extracted_content`.

    doc_artifact = types.Part(
        inline_data=types.Blob(
            mime_type="text/plain", data=extracted_content.encode("utf-8")
        )
    )

    # TODO: 2. Save the part as an artifact named f"{document_name}_extracted.txt".

    artifact_name = f"{document_name}_extracted.txt"

    # save_artifact returns the version number
    version = await tool_context.save_artifact(artifact_name, doc_artifact)

    # TODO: 3. Return a confirmation message including the new version number.
    return f"Extraction complete. Saved '{artifact_name}' version {version}."


async def summarize_document(document_name: str, tool_context: ToolContext) -> str:
    """Generates a summary of a document from its extracted text artifact."""
    # TODO: 1. Load the latest version of the f"{document_name}_extracted.txt" artifact.
    # TODO: 2. If the artifact is not found, return a helpful error message.

    summary_content = f"This is a concise summary of the document '{document_name}'."

    # TODO: 3. Create a types.Part from the `summary_content`.

    part = types.Part(text=summary_content)

    # TODO: 4. Save the summary as a new artifact named f"{document_name}_summary.txt".

    version = await tool_context.save_artifact(
        filename=f"{document_name}_summary.txt", artifact=part
    )
    # TODO: 5. Return a confirmation message.
    return f"Summary created as version {version}"


async def create_report(document_name: str, tool_context: ToolContext) -> str:
    """Creates a final report by compiling all artifacts for a document."""
    # TODO: 1. List all available artifacts using the tool_context.

    try:
        artifacts = await tool_context.list_artifacts()
    except Exception:
        # If listing fails, return a clear message
        return "Failed to list artifacts."

    # TODO: 2. Filter the list to get only the names of artifacts for the current document.

    artifact_names = []
    for a in artifacts:
        if document_name in a.name:
            artifact_names.append(a.name)

    # TODO: 3. Loop through your filtered list of artifact names. In the loop,
    # load each artifact and append its name and content to the `report` string.

    report = f"# Final Report for Document: {document_name}\n\n"

    for name in sorted(artifact_names):
        try:
            part = await tool_context.load_artifact(name)
        except Exception:
            part = None

        content = ""
        if part:
            try:
                blob = getattr(part, "inline_data", None)
                raw = getattr(blob, "data", None)
                if isinstance(raw, (bytes, bytearray)):
                    content = raw.decode("utf-8", errors="replace")
                elif isinstance(raw, str):
                    content = raw
                else:
                    content = str(raw)
            except Exception:
                content = "<unable to read artifact content>"

    report += f"## Artifact: {name}\n\n{content}\n\n---\n\n"

    # TODO: 4. Save the final `report` string as an artifact named
    # f"{document_name}_FINAL_REPORT.md".

    report_part = types.Part(
        inline_data=types.Blob(mime_type="text/markdown", data=report.encode("utf-8"))
    )

    final_report = f"{document_name}_FINAL_REPORT.md"

    try:
        saved_report = await tool_context.save_artifact(final_report, report_part)
    except AttributeError:
        saved_report = await tool_context.create_artifact(final_report, report_part)
    except Exception:
        return f"Failed to save final report '{final_report}'."

    # TODO: 5. Return a confirmation message.
    report_version = (
        getattr(saved_report, "version", None)
        or getattr(saved_report, "latest_version", None)
        or "unknown"
    )
    return f"Report complete. Saved '{final_report}' version {report_version}."


# ============================================================================
# AGENT DEFINITION
# ============================================================================

# TODO: Define the `root_agent`. Give it an instruction that tells it to run the
# pipeline in the correct order (extract -> summarize -> report) and register
# the three async tools.
root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Document processing agent that extracts text, summarizes content, and creates reports.",
    instruction="""
    You are a document processing agent that handles documents by extracting text, summarizing content, and creating final reports.
    """,
    tools=[
        extract_text,
        summarize_document,
        create_report,
    ],
    # output_key="",
)
