import logging
import tiktoken
from typing import List, Dict
from abstract.prompt_builder import PromptBuilder

class PromptBuilder(PromptBuilder):
    def __init__(self, model: str, max_tokens: int = 4096):
        self.model = model
        self.max_tokens = max_tokens
        self.tokenizer = tiktoken.encoding_for_model(self.model)

    def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        tokens = 0
        for msg in messages:
            tokens += len(self.tokenizer.encode(msg["content"])) + 4
        return tokens

    def build_messages(
        self, 
        system_message: str, 
        n_shots: List[Dict[str, str]], 
        memory: List[Dict[str, str]], 
        user_input: str
    ) -> List[Dict[str, str]]:
        messages = [{"role": "system", "content": system_message}]

        # Add few-shot examples
        for example in n_shots:
            messages.append({"role": "user", "content": example["user"]})
            messages.append({"role": "assistant", "content": example["assistant"]})

        # Add memory
        for entry in memory:
            # Memory entries already have a 'role' and 'content'
            # Ensure consistent format
            messages.append({"role": entry["role"], "content": entry["content"]})

        # Add current user query
        messages.append({"role": "user", "content": user_input})

        # Check token count
        token_count = self.count_tokens(messages)
        if token_count > self.max_tokens:
            logging.warning(
                f"Message exceeds max token limit ({self.max_tokens}). Current count: {token_count}. "
                "Consider truncating memory."
            )
            # Implement a truncation strategy here if needed.
            raise ValueError("Exceeds max token limit.")

        return messages
