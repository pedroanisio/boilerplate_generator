import logging
import os
from openai import OpenAI
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

class LLMBrain:
    """
    Holds configuration and parameters for the LLM.
    """
    def __init__(self, model_type: str = "gpt-4", temperature: float = 0.7, max_tokens: int = 4096):
        logging.debug(f"Initializing LLMBrain with model: {model_type}, temp: {temperature}, max_tokens: {max_tokens}")
        self.model_type = model_type
        self.temperature = temperature
        self.max_tokens = max_tokens
        # Initialize the OpenAI client
        try:
            api_key = os.getenv("OPENAI_API_KEY")  # Load API key from .env file
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set in environment variables")
            client = OpenAI(api_key=api_key)
            logging.info("OpenAI client initialized successfully")
            self.client = client
        except Exception as e:
            logging.critical(f"Failed to initialize OpenAI client: {e}")
            exit(1)
