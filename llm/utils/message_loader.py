import logging
import os
from typing import List, Dict
from llm.abstract.message_loader import MessageLoader

class MessageLoader(MessageLoader):
    def load_system_message(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            logging.error(f"System message file not found: {file_path}")
            raise FileNotFoundError(f"{file_path} not found.")

        with open(file_path, "r") as file:
            system_msg = file.read().strip()

        if not system_msg:
            logging.warning("System message file is empty.")
        return system_msg

    def load_n_shots(self, file_path: str) -> List[Dict[str, str]]:
        """
        Loads n-shot examples from a file.

        Args:
            file_path (str): Path to the n-shots file.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing user and assistant pairs.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file content is malformed.
        """
        if not os.path.exists(file_path):
            logging.error(f"N-shots file not found: {file_path}")
            raise FileNotFoundError(f"{file_path} not found.")

        examples = []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]
            
            if len(lines) % 2 != 0:
                logging.error("The file does not contain an even number of lines. Each user prompt must have a corresponding assistant response.")
                raise ValueError("Malformed n-shots file: Uneven number of lines.")

            for i in range(0, len(lines), 2):
                user = lines[i].lstrip("User:").strip()  # Remove any "User:" prefix if present
                assistant = lines[i + 1].lstrip("Assistant:").strip()  # Remove any "Assistant:" prefix if present
                examples.append({"user": user, "assistant": assistant})

        except Exception as e:
            logging.error(f"Error while reading n-shots file: {e}")
            raise e

        return examples
