import os
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# ── Tool function ──────────────────────────────────────────
def summarize_text(text: str) -> dict:
    """
    Accepts a block of text and returns it for the agent to summarize.

    Args:
        text: The text content to summarize.
    Returns:
        A dict containing the original text and its word count.
    """
    return {
        "original_text": text,
        "word_count": len(text.split())
    }

# ── Register tool ──────────────────────────────────────────
summarize_tool = FunctionTool(func=summarize_text)

# ── ADK Agent ─────────────────────────────────────────────
root_agent = Agent(
    name="summarizer_agent",
    model="gemini-2.5-flash-lite",       # free tier Gemini model
    description="An AI agent that summarizes text into concise sentences.",
    instruction="""You are a helpful text summarization assistant.
    When the user provides text:
    1. Call the summarize_text tool with the provided text
    2. Then write a clear, concise summary in 2-3 sentences
    3. Highlight the key points from the original text
    Always be accurate and professional.""",
    tools=[summarize_tool],
)