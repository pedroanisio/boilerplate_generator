## path : memory/composite_memory.py
from typing import List, Dict
from memory.abstract_memory import AbstractMemory

class CompositeMemory(AbstractMemory):
    """
    Composite memory implementation.
    Combines short-term and long-term memory systems.
    """

    def __init__(self, short_term_memory: AbstractMemory, long_term_memory: AbstractMemory):
        self.short_term_memory = short_term_memory
        self.long_term_memory = long_term_memory

    def add_interaction(self, user_message: str, assistant_response: str) -> None:
        """
        Add an interaction to both short-term and long-term memory.
        """
        self.short_term_memory.add_interaction(user_message, assistant_response)
        self.long_term_memory.add_interaction(user_message, assistant_response)

    def retrieve(self) -> List[Dict[str, str]]:
        """
        Retrieve combined memory from both short-term and long-term memory.

        Short-term interactions are prioritized.
        """
        short_term = self.short_term_memory.retrieve()
        long_term = self.long_term_memory.retrieve()
        return short_term + long_term

    def clear(self) -> None:
        """
        Clear both short-term and long-term memory.
        """
        self.short_term_memory.clear()
        self.long_term_memory.clear()
