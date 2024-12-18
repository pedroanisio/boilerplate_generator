import json
import logging
from llm.llm_brain import LLMBrain
from llm.memory.short_term_memory import ShortTermMemory
from llm.memory.long_term_memory import LongTermMemory
from llm.memory.composite_memory import CompositeMemory
from llm.persona import Persona

class AIManager:
    """
    Centralized manager for AI components.
    Handles initialization, configuration, and interaction with the LLM and Persona.
    """

    def __init__(self, config_path: str):
        """
        Initialize the AI Manager with a given configuration file path.
        
        :param config_path: Path to the JSON configuration file.
        """
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.llm_brain = None
        self.memory = None
        self.persona = None
        self._initialize_components()

    def _load_config(self, path: str) -> dict:
        """
        Load the configuration file.
        
        :param path: Path to the configuration file.
        :return: Parsed configuration dictionary.
        """
        try:
            with open(path, "r") as f:
                logging.info(f"Loading configuration from {path}")
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {path}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding configuration file: {e}")
            raise

    def _initialize_components(self):
        """
        Initialize the AI components: LLMBrain, Memory, and Persona.
        """
        # Initialize LLMBrain
        self.llm_brain = LLMBrain(
            model_type=self.config["model_name"],
            max_tokens=self.config["max_tokens"]
        )
        logging.info("LLMBrain initialized.")

        # Initialize memory
        short_term_memory = ShortTermMemory(max_length=5)
        long_term_memory = LongTermMemory()
        self.memory = CompositeMemory(short_term_memory, long_term_memory)
        logging.info("Memory components initialized.")

        # Initialize Persona
        self.persona = Persona(
            llm_brain=self.llm_brain,
            memory=self.memory,
            config=self.config
        )
        logging.info("Persona initialized.")

    def interact(self, user_input: str) -> str:
        """
        Process user input and get a response from the Persona.
        
        :param user_input: Input query from the user.
        :return: Response from the Persona.
        """
        logging.info(f"Processing user input: {user_input}")
        try:
            response = self.persona.respond_to(user_input)
            logging.info("Response generated successfully.")
            return response
        except Exception as e:
            logging.error(f"Error during interaction: {e}", exc_info=True)
            raise

    def reflect(self):
        """
        Trigger the reflection process for the Persona.
        """
        logging.info("Initiating reflection process.")
        try:
            self.persona.reflect()
            logging.info("Reflection completed successfully.")
        except Exception as e:
            logging.error(f"Reflection process failed: {e}", exc_info=True)
            raise

    def describe_persona(self) -> str:
        """
        Get a description of the Persona's current state.
        
        :return: Persona description.
        """
        logging.info("Describing persona state.")
        return self.persona.describe()

    def reload_config(self):
        """
        Reload the configuration file and reinitialize components.
        """
        logging.info("Reloading configuration.")
        self.config = self._load_config(self.config_path)
        self._initialize_components()
        logging.info("Components reinitialized.")


