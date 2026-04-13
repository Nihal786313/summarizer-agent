import os
import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent.agent import root_agent

app = FastAPI(title="ADK Summarizer Agent API")

# ADK session service
session_service = InMemorySessionService()
APP_NAME  = "summarizer_agent_app"
USER_ID   = "render_user"

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str
    status: str

@app.get("/")
def root():
    return {"message": "ADK Summarizer Agent is running!"}

@app.get("/health")
def health():
    return {"status": "healthy", "agent": "summarizer_agent", "framework": "Google ADK"}

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Create a fresh session per request (stateless)
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID
        )

        runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )

        # Send message to the ADK agent
        user_message = types.Content(
            role="user",
            parts=[types.Part(text=f"Please summarize this text: {request.text}")]
        )

        final_response = ""
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=user_message
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        final_response += part.text

        return SummarizeResponse(summary=final_response, status="success")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)