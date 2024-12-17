
class PromptUtils:
    @staticmethod
    def system_message(file_path: str) -> str:
        """
        Reads a file containing system message lines and combines them into a single string.
        
        :param file_path: Path to the file containing the system message.
        :return: A single string with all lines combined, separated by spaces.
        """
        try:
            with open(file_path, "r") as file:
                # Read and combine lines into a single string
                return " ".join(line.strip() for line in file.readlines())
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at '{file_path}' was not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the file: {e}")
