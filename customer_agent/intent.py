from typing import Tuple

class IntentAgent:
    def classify(self, message: str) -> Tuple[str, str]:
        # Simple heuristic classification
        msg = message.lower()
        
        intent = "general_inquiry"
        if any(w in msg for w in ["pay", "bill", "invoice", "charge", "refund", "credit"]):
            intent = "billing"
        elif any(w in msg for w in ["error", "bug", "fail", "broken", "login", "password"]):
            intent = "technical_issue"
            
        urgency = "low"
        if any(w in msg for w in ["urgent", "immediately", "asap", "now", "critical"]):
            urgency = "high"
        elif any(w in msg for w in ["quickly", "soon", "waiting"]):
            urgency = "medium"
            
        return intent, urgency
