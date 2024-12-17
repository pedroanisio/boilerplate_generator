## path : llm/abstract/memory.py
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union


class Memory(ABC):
    """
    Abstract base class for memory management.
    Provides the interface for storing and retrieving user-assistant interactions.
    """

    @abstractmethod
    def add_interaction(
        self, 
        user_message: str, 
        assistant_response: str, 
        metadata: Optional[Dict[str, Union[str, int, float]]] = None
    ) -> None:
        """
        Add a user-assistant interaction to memory.

        :param user_message: The user's input message.
        :param assistant_response: The assistant's response.
        :param metadata: Optional metadata associated with the interaction (e.g., timestamp, tags).
        """
        pass

    @abstractmethod
    def retrieve(
        self, 
        role: Optional[str] = None, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Union[str, Dict]]]:
        """
        Retrieve memory contents.

        :param role: Filter interactions by role ('user', 'assistant', 'system').
        :param limit: Number of recent interactions to retrieve.
        :return: A list of memory entries, each entry as a dictionary with keys 'role', 'content', and optional 'metadata'.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clear the memory.
        """
        pass
