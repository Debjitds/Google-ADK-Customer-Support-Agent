import argparse
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from customer_agent.coordinator import Coordinator


class AskBody(BaseModel):
    message: str


def run_cli(message: str, model: Optional[str], api_key: Optional[str]):
    c = Coordinator((model or "gemini-2.5-flash"), api_key)
    out = c.ask(message)
    print(out)


def run_server(model: Optional[str], host: str, port: int, api_key: Optional[str]):
    c = Coordinator((model or "gemini-2.5-flash"), api_key)
    app = FastAPI()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/ask")
    def ask(body: AskBody):
        return c.ask(body.message)

    uvicorn.run(app, host=host, port=port)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("message", nargs="?", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--server", action="store_true")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.server:
        run_server(args.model, args.host, args.port, args.api_key)
    else:
        if not args.message:
            raise SystemExit("message is required for CLI mode")
        run_cli(args.message, args.model, args.api_key)


if __name__ == "__main__":
    main()