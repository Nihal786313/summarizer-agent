import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import summarize

app = FastAPI(title="Summarizer Agent API")

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str
    status: str

@app.get("/")
async def root():
    return {"message": "Summarizer Agent is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_endpoint(request: SummarizeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    try:
        result = summarize(request.text)
        return SummarizeResponse(summary=result, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)