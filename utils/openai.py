import logging
from abc import ABC, abstractmethod
from typing import Any
from abstract.ai_engine import AbstractAIEngine

class OpenAIEngine(AbstractAIEngine):
    def __init__(self, client: Any):
        """
        Initializes the OpenAIEngine with a client for making API requests.

        :param client: The OpenAI client.
        """
        logging.debug("Initializing OpenAIEngine")
        super().__init__()
        self.client = client

    def complete(self, flavor: Any) -> str:
        """
        Sends a completion request to the OpenAI API based on the given flavor.

        :param flavor: An object containing model, system_message, and user_message.
        :return: The generated completion as a string.
        """
        if not hasattr(flavor, "model") or not hasattr(flavor, "system_message") or not hasattr(flavor, "user_message"):
            raise ValueError("Flavor must have 'model', 'system_message', and 'user_message' attributes.")
        
        logging.debug(f"Sending completion request with model: {flavor.model}")
        try:
            completion = self.client.chat.completions.create(
                model=flavor.model,
                messages=[
                    {"role": "system", "content": flavor.system_message},
                    {"role": "user", "content": flavor.user_message},
                ],
            )
            logging.debug("Completion request successful")
            return completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Error during completion: {e}")
            raise RuntimeError(f"Failed to complete request: {e}") from e

class Fuel:
    """
    Represents the "fuel" or model type to be used by the AI system.
    """
    def __init__(self, f_type="gpt-4"):
        logging.debug(f"Initializing Fuel with type: {f_type}")
        self.f_type = f_type


class Flavor:
    """
    Holds the configuration (model), system message, and user message for a prompt.
    """
    def __init__(self, model="gpt-4"):
        logging.debug(f"Initializing Flavor with model: {model}")
        self.model = model
        self.system_message = ""
        self.user_message = ""

    def set_sys_msg(self, message: str):
        """
        Set the system (context) message.
        """
        logging.debug(f"Setting system message: {message}")
        self.system_message = message

    def set_user_msg(self, message: str):
        """
        Set the user message (the query or instruction from the user).
        """
        logging.debug(f"Setting user message: {message}")
        self.user_message = message

## first message is always the system message
## n_shots is a stack of user messages and "assistant" responses used for training
## memory is a stack of user messages and "assistant" responses relevant to the current conversation
## users_input is always the last message


class Tools:
    """
    A utility class providing file operations and command processing.
    """
    def __init__(self):
        logging.debug("Initializing Tools")

    def read_file(self, filename: str) -> str:
        """
        Read the contents of a file.
        """
        logging.debug(f"Reading file: {filename}")
        try:
            with open(filename, "r") as file:
                content = file.read()
            logging.info(f"File read successfully: {filename}")
            return content
        except Exception as e:
            logging.error(f"Error reading file: {e}")
            return f"Error: {e}"

    def show_read_file(self) -> str:
        """
        Provide instructions on how to request a file read.
        """
        return "You can request a file read using the following command: /readfile, filename"

    def show_list_dir(self) -> str:
        """
        Provide instructions on how to list files in a directory.
        """
        return "You can list the files in the directory using the following command: /ls"

    def list_dir(self) -> str:
        """
        List files in the 'ai_files' directory.
        """
        logging.debug("Listing files in the directory")
        try:
            files = os.listdir("ai_files")
            logging.info("Files listed successfully")
            return str(files)
        except Exception as e:
            logging.error(f"Error listing files: {e}")
            return f"Error: {e}"

    def create_file(self, filename: str, content: str) -> str:
        """
        Create a file with the given filename and content in the 'ai_files' directory.
        """
        logging.debug(f"Creating file: {filename} with content: {content}")
        try:
            directory = "ai_files"
            if not os.path.exists(directory):
                os.makedirs(directory)
            filepath = os.path.join(directory, filename)
            with open(filepath, "w") as file:
                file.write(content)
            logging.info(f"File created: {filepath}")
            return filepath
        except Exception as e:
            logging.error(f"Error creating file: {e}")
            return f"Error: {e}"

    def process_message(self, message: str) -> str:
        """
        Process a command message from the AI and perform the requested action.
        Commands:
          - /createfile, filename, content
          - /readfile, filename
          - /ls
        """
        logging.debug(f"Processing message: {message}")

        if message.startswith("/createfile"):
            try:
                # Format: /createfile, filename, content
                parts = message.split(", ", 2)
                if len(parts) != 3:
                    return "Invalid command format"
                _, filename, content = parts
                return self.create_file(filename, content)
            except ValueError as e:
                logging.error(f"Message parsing error: {e}")
                return "Invalid command format"

        if message.startswith("/readfile"):
            try:
                # Format: /readfile, filename
                parts = message.split(", ", 1)
                if len(parts) != 2:
                    return "Invalid command format"
                _, filename = parts
                return self.read_file(filename)
            except ValueError as e:
                logging.error(f"Message parsing error: {e}")
                return "Invalid command format"

        if message.startswith("/ls"):
            return self.list_dir()

        return "Invalid command"


class System_Message:
    """
    Collects multiple system messages and provides them as a single combined message.
    """
    def __init__(self):
        self.message = ""

    def add_message(self, message: str):
        self.message += message + "\n"

    def get_message(self) -> str:
        return self.message.strip()


if __name__ == "__main__":
    # Initialize the OpenAI client
    try:
        api_key = os.getenv("OPENAI_API_KEY")  # Load API key from .env file
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment variables")
        client = OpenAI(api_key=api_key)
        logging.info("OpenAI client initialized successfully")
    except Exception as e:
        logging.critical(f"Failed to initialize OpenAI client: {e}")
        exit(1)

    # Initialize utility classes
    tools = Tools()
    system = System_Message()

    # Set initial system messages
    system.add_message("You are a useful AI assistant.")
    system.add_message("You can code, inspect files, and create new files.")
    system.add_message("You can list the files in the directory using: /ls")
    system.add_message("You can request a file read using: /readfile, filename")
    system.add_message("You can request file creation using: /createfile, filename, content")
    system.add_message("If no command is given, you can execute the list files command.")

    # Prepare Flavor
    flavor = Flavor()
    flavor.set_sys_msg(system.get_message())
    flavor.set_user_msg("/ls")

    # Create engine and get response
    engine = OpenAIEngine(client)
    response = engine.complete(flavor)
    logging.info(f"Received response: {response}")

    # Process response as a command if applicable
    tools.process_message(str(response))

    logging.info("Script execution completed")
