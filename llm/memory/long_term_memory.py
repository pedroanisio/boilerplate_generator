## path : memory/long_term_memory.py
from typing import List, Dict
from memory.abstract_memory import AbstractMemory

class LongTermMemory(AbstractMemory):
    """
    Long-term memory implementation.
    Stores interactions persistently.
    """

    def __init__(self):
        self.memory = []

    def add_interaction(self, user_message: str, assistant_response: str) -> None:
        """
        Add an interaction to long-term memory.
        """
        self.memory.append({"user": user_message, "assistant": assistant_response})

    def retrieve(self) -> List[Dict[str, str]]:
        """
        Retrieve all stored interactions in long-term memory.
        """
        return self.memory

    def clear(self) -> None:
        """
        Clear the long-term memory.
        """
        self.memory = []
