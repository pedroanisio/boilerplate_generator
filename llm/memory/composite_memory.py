from typing import List, Dict, Optional, Union
from llm.abstract.abstract_memory import AbstractMemory

class CompositeMemory(AbstractMemory):
    def __init__(self, short_term_memory: AbstractMemory, long_term_memory: AbstractMemory):
        self.short_term_memory = short_term_memory
        self.long_term_memory = long_term_memory

    def add_interaction(
        self, 
        user_message: str, 
        assistant_response: str, 
        metadata: Optional[Dict[str, Union[str, int, float]]] = None
    ) -> None:
        self.short_term_memory.add_interaction(user_message, assistant_response, metadata=metadata)
        self.long_term_memory.add_interaction(user_message, assistant_response, metadata=metadata)

    def retrieve(
        self, role: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Dict[str, Union[str, Dict]]]:
        # Combining memory. You might want a smarter merge strategy here.
        st = self.short_term_memory.retrieve(role=role)
        lt = self.long_term_memory.retrieve(role=role)
        return st + lt

    def clear(self) -> None:
        self.short_term_memory.clear()
        self.long_term_memory.clear()
