from typing import Dict

from .intent import IntentAgent
from .reply import ReplyAgent
from .escalation import EscalationAgent
from .memory import Memory


class Coordinator:
    def __init__(self, model_name: str = "gemini-2.5-flash", api_key: str | None = None):
        self.intent_agent = IntentAgent()
        # Initialize reply agent with specific model and key
        self.reply_agent = ReplyAgent(model_name, api_key)
        self.escalation_agent = EscalationAgent()
        self.memory = Memory()

    def ask(self, message: str) -> Dict:
        # Add user message to memory
        self.memory.add("user", message)
        
        # 1. Classify Intent and Urgency
        intent, urgency = self.intent_agent.classify(message)
        
        # 2. Get Context
        context = self.memory.get_context()
        
        # 3. Generate Reply
        reply = self.reply_agent.create_reply(message, intent, urgency, context)
        
        # 4. Check for Escalation
        escalation = self.escalation_agent.check(intent, urgency, message)
        
        out = {"intent": intent, "urgency": urgency, "reply": reply, "escalation": escalation}
        
        # Add agent reply to memory
        self.memory.add("agent", reply)
        return out
