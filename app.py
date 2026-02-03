import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from customer_agent.coordinator import Coordinator

app = FastAPI()

def get_coordinator():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set")

    return Coordinator(
        model_name=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        api_key=api_key,
    )

class AskBody(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "Customer agent is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(body: AskBody):
    try:
        coordinator = get_coordinator()
        reply = coordinator.ask(body.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
