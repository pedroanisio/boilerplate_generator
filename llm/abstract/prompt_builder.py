from abc import ABC, abstractmethod
from typing import List, Dict

class PromptBuilder(ABC):
    @abstractmethod
    def build_messages(
        self, 
        system_message: str, 
        n_shots: List[Dict[str, str]], 
        memory: List[Dict[str, str]], 
        user_input: str
    ) -> List[Dict[str, str]]:
        pass
