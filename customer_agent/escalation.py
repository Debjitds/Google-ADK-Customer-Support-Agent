from typing import Dict, Any

class EscalationAgent:
    def check(self, intent: str, urgency: str, message: str) -> Dict[str, Any]:
        escalate = False
        note = "No escalation required."
        
        if urgency == "high":
            escalate = True
            note = f"High urgency {intent} issue detected."
            
        if "lawyer" in message.lower() or "sue" in message.lower():
            escalate = True
            note = "Legal threat detected."
            
        return {"escalate": escalate, "note": note}
