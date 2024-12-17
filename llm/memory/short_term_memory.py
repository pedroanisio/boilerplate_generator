## path : llm/memory/short_term_memory.py
from typing import List, Dict, Optional, Union
from llm.abstract.memory import Memory


class ShortTermMemory(Memory):
    """
    Short-term memory implementation.
    Stores recent interactions up to a specified maximum length.
    """

    def __init__(self, max_length: int = 5):
        self.max_length = max_length
        self.memory = []  # Store interactions as a list of dictionaries

    def add_interaction(
        self, 
        user_message: str, 
        assistant_response: str, 
        metadata: Optional[Dict[str, Union[str, int, float]]] = None
    ) -> None:
        """
        Add a user-assistant interaction to short-term memory.
        """
        interaction = [
            {"role": "user", "content": user_message, "metadata": metadata},
            {"role": "assistant", "content": assistant_response, "metadata": metadata},
        ]
        self.memory.extend(interaction)
        if len(self.memory) > self.max_length:
            self.memory = self.memory[-self.max_length:]  # Retain only the most recent entries

    def retrieve(
        self, role: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Dict[str, Union[str, Dict]]]:
        """
        Retrieve memory contents with optional role filtering and limit.
        """
        filtered_memory = self.memory
        if role:
            filtered_memory = [entry for entry in self.memory if entry["role"] == role]
        if limit:
            filtered_memory = filtered_memory[-limit:]
        return filtered_memory

    def clear(self) -> None:
        """
        Clear the short-term memory.
        """
        self.memory = []
