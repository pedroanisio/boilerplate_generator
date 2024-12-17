import logging
import openai
from typing import List, Dict
from llm.abstract.llm_provider import LLMProvider 

class LLMProvider(LLMProvider):
    """
    Handles interaction with the underlying LLM (e.g., OpenAI).
    """
    def __init__(self, model: str, temperature: float = 0.7):
        self.model = model
        self.temperature = temperature

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                top_p=1.0
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.error(f"Error calling LLM API: {e}")
            raise
