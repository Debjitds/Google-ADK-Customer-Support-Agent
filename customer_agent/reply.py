import os
from typing import Optional


class ReplyAgent:
    def __init__(self, model_name: str = "gemini-2.5-flash", api_key: Optional[str] = None):
        # Prioritize passed key, then env var
        key = api_key or os.getenv("GOOGLE_API_KEY")
        if not key:
            # It's possible the user environment isn't set up right if we get here
            # But the coordinator handles retrieval usually.
            pass 
        
        if key:
            os.environ["GOOGLE_API_KEY"] = key
            
        self._use_adk = False
        self.model_name = model_name
        self.key = key
        
        try:
            # Try to use ADK if available and configured
            from google.adk.agents import LlmAgent
            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService
            from google.genai import types as genai_types
            
            self._adk_types = genai_types
            self._adk_session_service = InMemorySessionService()
            self._adk_agent = LlmAgent(name="ReplyAgent", model=model_name, instruction="You are a customer support assistant. Use a concise, professional tone.")
            self._adk_runner = Runner(agent=self._adk_agent, app_name="cust_app", session_service=self._adk_session_service)
            self._adk_user_id = "user"
            self._adk_session_id = "reply_session"
            self._adk_session_service.create_session(app_name="cust_app", user_id=self._adk_user_id, session_id=self._adk_session_id)
            self._use_adk = True
        except Exception:
            # Fallback to direct genai usage
            import google.generativeai as genai
            if key:
                genai.configure(api_key=key)
            self.model = genai.GenerativeModel(model_name)

    def create_reply(self, message: str, intent: str, urgency: str, context: Optional[str] = None) -> str:
        prompt = (
            "You are a customer support assistant. "
            "Use a concise, professional tone. "
            "Provide clear steps and request one piece of missing information if needed. "
            f"Intent: {intent}. Urgency: {urgency}. "
            f"Conversation context:\n{context or ''}\n"
            f"User message:\n{message}\n"
            "Write a single reply suitable to send to the customer."
        )
        
        if self._use_adk:
            try:
                content = self._adk_types.Content(role="user", parts=[self._adk_types.Part(text=prompt)])
                events = self._adk_runner.run(user_id=self._adk_user_id, session_id=self._adk_session_id, new_message=content)
                for e in events:
                    try:
                        if e.is_final_response():
                            if e.content and e.content.parts:
                                return e.content.parts[0].text
                    except Exception:
                        pass
                return "Thanks for reaching out. Could you share more details?"
            except Exception:
                return "Thanks for reaching out. We’re experiencing a connection issue. Please share more details and we’ll follow up shortly."
        else:
            try:
                r = self.model.generate_content(prompt)
                return getattr(r, "text", "") or "Thanks for reaching out. Could you share more details?"
            except Exception:
                return "Thanks for reaching out. We’re experiencing a connection issue. Please share more details and we’ll follow up shortly."
