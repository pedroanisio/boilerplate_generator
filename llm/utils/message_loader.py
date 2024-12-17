import logging
import os
from typing import List, Dict
from abstract.message_loader import MessageLoader

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
        if not os.path.exists(file_path):
            logging.error(f"N-shots file not found: {file_path}")
            raise FileNotFoundError(f"{file_path} not found.")

        with open(file_path, "r") as file:
            lines = [l.strip() for l in file.readlines() if l.strip()]

        examples = []
        for i in range(0, len(lines), 2):
            user = lines[i]
            assistant = lines[i+1] if i+1 < len(lines) else ""
            examples.append({"user": user, "assistant": assistant})

        return examples
