# Customer Support Agent (Google AI SDK + ADK)

A compact customer support agent that uses Google Gemini models and the Google ADK (Agent Development Kit) to classify messages, generate replies, and escalate when needed. This README focuses on the problem the agent solves, how it solves it, architecture, installation, running the ADK browser UI, conclusion, and the value the project delivers.

## 1. Problem Statement
Without an automated support agent:
- Manual triage causes slow responses, inconsistent categorization, and high average handle time (AHT).
- Agents lose context across interactions, causing repetitive questions and longer resolution times.
- Escalations are often ad-hoc or delayed, which harms SLAs and customer satisfaction.
- Small teams struggle to handle peak volumes, causing backlogs and revenue impact from unresolved issues.

Quantified impacts (typical):
- Increased AHT and missed SLAs
- Lower CSAT and higher churn
- Inefficient specialist routing and longer time-to-resolution

## 2. Solution Statement
This project provides:
- Automated intent detection and urgency scoring for consistent triage.
- ADK-integrated reply generation for event-driven, reproducible agent behavior.
- Built-in escalation rules to surface high-urgency cases to humans automatically.
- Lightweight memory to maintain short-term context and avoid repetitive prompts.
Together these reduce manual work, increase consistency, and accelerate resolution.

## 3. Architecture
High level flow:
```
User message
    ↓
Coordinator (orchestrates agents)
    ↓
IntentAgent → Memory (context)
    ↓
ReplyAgent (ADK runner or Generative SDK) → Response
    ↓
EscalationAgent (applies escalation rules) → Human queue (if needed)
```

Components:
- Coordinator: Orchestrates sub-agents and aggregates outputs.
- IntentAgent: Classifies message intent and urgency.
- Memory: Stores recent turns to preserve context.
- ReplyAgent: Generates responses via ADK flows or direct SDK calls.
- EscalationAgent: Evaluates escalation criteria and marks cases.

## 4. Install Process

Prerequisites
- Python 3.10+
- pip
- Network access for Gemini models
- Google API key (GOOGLE_API_KEY from Google AI Studio)
- Optional: Google ADK for browser UI (recommended for dev)

Quick install
```bash
# From project root
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.\.venv\Scripts\Activate.ps1 # Windows PowerShell

pip install -r requirements.txt
```

Environment variables
```bash
# Linux/macOS
export GOOGLE_API_KEY="YOUR_API_KEY"
# Windows PowerShell (session)
$env:GOOGLE_API_KEY = "YOUR_API_KEY"
# Windows persistent (PowerShell)
setx GOOGLE_API_KEY "YOUR_API_KEY"
```

Verification
```bash
# Run unit tests
python -m pytest -q

# Quick CLI test (example)
python app.py "My invoice is wrong." --api-key $GOOGLE_API_KEY
```

## 5. How to run adk_agent browser
The ADK browser provides a developer UI to run and inspect agent flows.

Install / verify ADK
```bash
pip install google-adk
pip show google-adk
```

Start ADK web UI (development)
```bash
# From project root
adk web --port 8000 --no-reload
# Open in browser:
http://localhost:8000
# In the UI, select the 'cust_support' agent (or equivalent)
```

Tips
- If ADK CLI is not on PATH, run via the Python module: python -m google_adk.cli web --port 8000
- For local debugging, run the Coordinator and server first:
  python app.py --server --api-key <YOUR_API_KEY>
- Use the ADK UI to execute events, inspect logs, and step through flows.

## 6. How to run the agent (CLI and Server)
CLI (single message)
```bash
python app.py "I need a refund" --api-key <YOUR_API_KEY>
```

HTTP server (FastAPI)
```bash
python app.py --server --api-key <YOUR_API_KEY> --host 127.0.0.1 --port 8000
# Health: http://127.0.0.1:8000/health
# Ask: POST http://127.0.0.1:8000/ask  { "message": "..." }
```

Common flags
- --model : choose Gemini model (default: gemini-2.5-flash)
- --api-key : pass API key inline instead of env var
- --server / --host / --port : start HTTP server

## 7. Conclusion
This agent reduces triage time, enforces consistent responses, and automates escalation for urgent issues. It is lightweight, easy to run locally, and integrates with ADK for observable, debuggable flows.

## 8. Value Statement
By deploying this agent you can expect:
- Faster average handle time (AHT) through automated triage and reply generation
- More consistent and contextual responses that increase CSAT
- Earlier and more accurate escalations, improving SLA compliance
- Reduced manual load on support teams so specialists focus on high-value work

## Project layout (quick)
```
customer_agent/
  __init__.py
  memory.py
  intent.py
  reply.py
  escalation.py
  coordinator.py
adk_agent/
  __init__.py
  agent.py
app.py
requirements.txt
tests/
  test_core.py
```

## Notes
- Keep API keys out of source control.
- Use ADK browser for interactive development; use server/CLI for automated runs.
- For production, deploy behind secure infrastructure and rotate keys regularly.