import logging
import openai
from typing import List, Dict
from llm.abstract.llm_provider import LLMProvider

class LLMProvider(LLMProvider):
    """
    Handles interaction with the LLM (e.g., OpenAI).
    """

    def __init__(self, model: str, temperature: float = 0.7, client=None):
        self.model = model
        self.temperature = temperature
        self.client = client

        # Set up a dedicated logger for this class
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)  # Adjust logging level as needed

        # Log initialization details
        self.logger.info(f"LLMProvider initialized with model={model}, temperature={temperature}")

    def generate(self, messages: List[Dict[str, str]]) -> str:
        """
        Generates a response using the LLM based on the provided messages.

        :param messages: List of role-based messages for the LLM.
        :return: The generated response from the LLM.
        """
        self.logger.debug(f"Generating response with model={self.model}, temperature={self.temperature}")
        self.logger.debug(f"Input messages: {messages}")

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                top_p=1.0
            )

            # Extract and log the response
            response = completion.choices[0].message.content.strip()
            self.logger.info("Response generated successfully")
            self.logger.debug(f"Generated response: {response}")
            return response

        except Exception as e:
            self.logger.error("Error occurred while generating response", exc_info=True)
            raise
