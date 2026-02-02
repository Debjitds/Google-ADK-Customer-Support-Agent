import argparse
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from customer_agent.coordinator import Coordinator

# Load environment variables (critical for Vercel if not using dashboard env vars, 
# but definitely needed for local dev)
load_dotenv()

# --- Global Instances for Vercel ---
# Vercel needs to be able to import 'app' directly.
app = FastAPI()

# We initialize the coordinator globally so it's ready for requests.
# It will use GOOGLE_API_KEY from environment.
coordinator = Coordinator(
    model_name=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    api_key=os.getenv("GOOGLE_API_KEY") # Can be None if set in env
)

class AskBody(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(body: AskBody):
    return coordinator.ask(body.message)

# --- CLI Functions ---
def run_cli(message: str, model: Optional[str], api_key: Optional[str]):
    # Allow CLI overrides, but default to the global instance logic if arguments are missing
    # Note: For simplicity in CLI, we create a new coordinator if args differ, 
    # or just use the global one if args match. 
    # To be safe and support overrides, let's make a temp coordinator if needed.
    
    config_model = model or "gemini-2.5-flash"
    config_key = api_key or os.getenv("GOOGLE_API_KEY")
    
    local_coordinator = Coordinator(config_model, config_key)
    out = local_coordinator.ask(message)
    print(out)

def run_server(host: str, port: int):
    # Just run the global app instance
    uvicorn.run(app, host=host, port=port)

def main():
    parser = argparse.ArgumentParser(description="Customer Agent CLI")
    parser.add_argument("message", nargs="?", default=None, help="The message to send to the agent")
    parser.add_argument("--model", default=None, help="Gemini model to use")
    parser.add_argument("--api-key", default=None, help="Google API Key")
    parser.add_argument("--server", action="store_true", help="Run as HTTP server")
    parser.add_argument("--host", default="127.0.0.1", help="Host for server")
    parser.add_argument("--port", type=int, default=8000, help="Port for server")
    
    args = parser.parse_args()
    
    if args.server:
        run_server(args.host, args.port)
    else:
        if not args.message:
            # If no message and no server flag, print help
            parser.print_help()
            return
        run_cli(args.message, args.model, args.api_key)

if __name__ == "__main__":
    main()