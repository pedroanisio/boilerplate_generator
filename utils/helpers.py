import random
import re
import string
import subprocess


def to_snake_case(name: str) -> str:
    # Handle the first uppercase letter in sequences to avoid splitting acronyms poorly
    # This pattern finds transitions from a lowercase letter or digit to an uppercase letter and inserts an underscore.
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Now handle uppercase letters followed by lowercase or the end. 
    # This catches acronyms or multiple uppercase sequences.
    s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.lower()

class Project:
    """
    Utility class for generating project-specific names with flexible formatting.
    """
    GODs = [
        "zeus", "poseidon", "hades", "apollo", "ares", "hermes", "dionysus", 
        "hephaestus", "helios", "cronus", "jupiter", "neptune", "pluto", "mars",
        "mercury", "bacchus", "vulcan", "sol", "saturn", "odin", "thor", "loki", 
        "balder", "tyr", "freyr", "heimdall", "vidar", "hod", "njord", "ra", 
        "osiris", "set", "anubis", "horus", "thoth", "sobek", "khnum", "ptah", 
        "amon", "tupan", "jaci"
    ]

    ADJECTIVES = [
        "ancient", "bold", "brave", "bright", "clever", "cool", "curious", 
        "daring", "eager", "fancy", "fierce", "frosty", "gentle", "giant", 
        "glowing", "hidden", "jolly", "lucky", "mighty", "mysterious", "noble", 
        "proud", "quick", "quiet", "rapid", "shy", "silly", "silent", "sparkling", 
        "thrifty", "vivid", "wild", "wise"
    ]
    
    NOUNS = [
        "ant", "bear", "cat", "cloud", "crane", "dragon", "eagle", "falcon", 
        "fox", "hawk", "lion", "lotus", "mouse", "otter", "owl", "panther", 
        "phoenix", "python", "raven", "river", "shark", "sky", "sparrow", 
        "tiger", "walrus", "whale", "wolf", "zebra"
    ]

    @staticmethod
    def generate_random_name(format_string="{adjectives}-{nouns}-{digits}", transform=lambda x: x):
        """
        Generate a random name based on a flexible format string.
        
        Placeholders:
        - {adjective}: Random adjective
        - {gods}: Random god name
        - {noun}: Random noun
        - {digits}: Random two-digit number
        
        :param format_string: The format string to define the name structure.
        :param transform: A lambda function to transform the generated name.
        :return: A formatted project name string.
        """
        components = {
            "adjectives": random.choice(Project.ADJECTIVES),
            "gods": random.choice(Project.GODs),
            "nouns": random.choice(Project.NOUNS),
            "digits": ''.join(random.choices(string.digits, k=2))
        }
        
        # Replace placeholders in the format string with generated components
        name = re.sub(r"\{(\w+)\}", lambda match: components.get(match.group(1), ""), format_string)
        return transform(name)


    @staticmethod
    def generate_random_project_name():
        """
        Generate a random project name.

        :return: A random string of 8 alphanumeric characters.
        """
        return Project.generate_random_name("{adjectives}-{nouns}-{digits}")

    @staticmethod
    def generate_db_username():
        """
        Generate a random database username.

        :return: A random string of 6 alphanumeric characters.
        """
        return Project.generate_random_name("{gods}_{digits}")

    @staticmethod
    def generate_random_password(length=12):
        """
        Generate a secure random password.

        :param length: The length of the password (default is 12).
        :return: A random string of specified length containing letters, digits, and symbols.
        """
        characters = string.ascii_letters + string.digits + "^*-_+"
        return ''.join(random.choices(characters, k=length))

def chain_handlers(handlers):
    """
    Chains the handlers together.

    :param handlers: List of handlers to chain.
    :return: The head of the chain.
    """
    for i in range(len(handlers) - 1):
        handlers[i].set_next(handlers[i + 1])
    return handlers[0]  # Return the first handler in the chain


def run_command(command, description, cwd=None):
    """
    Execute a shell command with a description and optional working directory.

    :param command: The shell command to run.
    :param description: A brief description of the command.
    :param cwd: Optional directory to execute the command in.
    """
    print(f"Running: {description}")
    result = subprocess.run(command, shell=True, text=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Failed: {description}\n{result.stderr.strip()}")
        raise RuntimeError(f"Command failed: {description}")
    print(f"Success: {description} completed.")
