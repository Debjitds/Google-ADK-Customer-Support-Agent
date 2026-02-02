from customer_agent.intent import IntentAgent
from customer_agent.escalation import EscalationAgent


def test_intent_refund():
    ia = IntentAgent()
    intent, urgency = ia.classify("I need a refund")
    assert intent == "refund"
    assert urgency == "high"


def test_intent_billing():
    ia = IntentAgent()
    intent, urgency = ia.classify("My invoice is wrong")
    assert intent == "billing"
    assert urgency == "medium"


def test_escalation_high():
    ea = EscalationAgent()
    out = ea.check("refund", "high", "Please help urgently")
    assert out["escalate"] is True