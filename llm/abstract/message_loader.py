from abc import ABC, abstractmethod
from typing import List, Dict

class MessageLoader(ABC):
    
    @abstractmethod
    def load_system_message(self, file_path: str) -> str:
        pass

    @abstractmethod
    def load_n_shots(self, file_path: str) -> List[Dict[str, str]]:
        pass
