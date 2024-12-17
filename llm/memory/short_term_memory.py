from typing import List, Dict, Optional, Union
from llm.abstract.abstract_memory import AbstractMemory

class ShortTermMemory(AbstractMemory):
    def __init__(self, max_length: int = 5):
        self.max_length = max_length
        self.memory = []  # list of {"role": "user"/"assistant", "content": str, "metadata": dict}

    def add_interaction(
        self, 
        user_message: str, 
        assistant_response: str, 
        metadata: Optional[Dict[str, Union[str, int, float]]] = None
    ) -> None:
        user_entry = {"role": "user", "content": user_message, "metadata": metadata}
        assistant_entry = {"role": "assistant", "content": assistant_response, "metadata": metadata}
        self.memory.extend([user_entry, assistant_entry])

        # Truncate if necessary
        if len(self.memory) > self.max_length:
            self.memory = self.memory[-self.max_length:]

    def retrieve(
        self, role: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Dict[str, Union[str, Dict]]]:
        filtered = self.memory
        if role:
            filtered = [m for m in filtered if m["role"] == role]
        if limit:
            filtered = filtered[-limit:]
        return filtered

    def clear(self) -> None:
        self.memory.clear()
