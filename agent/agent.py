import os
import google.generativeai as genai

# Configure with free API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Use the free-tier friendly model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",  # Best free tier limits
    system_instruction="""You are a helpful text summarization assistant.
    When given text, provide a clear, concise summary in 2-3 sentences.
    Highlight the most important points."""
)

def summarize(text: str) -> str:
    """Summarize the given text using Gemini."""
    response = model.generate_content(
        f"Please summarize this text:\n\n{text}"
    )
    return response.text