from typing import List, Dict, Optional, Union
from llm.abstract.abstract_memory import AbstractMemory

class LongTermMemory(AbstractMemory):
    def __init__(self):
        self.storage = []  # Similar structure to ShortTermMemory

    def add_interaction(
        self, 
        user_message: str, 
        assistant_response: str, 
        metadata: Optional[Dict[str, Union[str, int, float]]] = None
    ) -> None:
        user_entry = {"role": "user", "content": user_message, "metadata": metadata}
        assistant_entry = {"role": "assistant", "content": assistant_response, "metadata": metadata}
        self.storage.extend([user_entry, assistant_entry])

    def retrieve(
        self, role: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Dict[str, Union[str, Dict]]]:
        filtered = self.storage
        if role:
            filtered = [m for m in filtered if m["role"] == role]
        if limit:
            filtered = filtered[-limit:]
        return filtered

    def clear(self) -> None:
        self.storage.clear()
