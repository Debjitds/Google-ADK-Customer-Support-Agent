from typing import List, Dict

class Memory:
    def __init__(self):
        self.history: List[Dict[str, str]] = []
        
    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        # Keep only last 10 turns
        if len(self.history) > 20:
            self.history = self.history[-20:]
            
    def get_context(self) -> str:
        return "\n".join([f"{h['role']}: {h['content']}" for h in self.history])
