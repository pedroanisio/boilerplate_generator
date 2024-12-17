import logging

class LLMBrain:
    """
    Holds configuration and parameters for the LLM.
    """
    def __init__(self, model_type: str = "gpt-4", temperature: float = 0.7, max_tokens: int = 4096):
        logging.debug(f"Initializing LLMBrain with model: {model_type}, temp: {temperature}, max_tokens: {max_tokens}")
        self.model_type = model_type
        self.temperature = temperature
        self.max_tokens = max_tokens
