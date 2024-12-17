import random
import string

class Project:
    """
    Utility class for generating project-specific details like database names and passwords.
    """

    @staticmethod
    def generate_random_project_name():
        """
        Generate a random project name.

        :return: A random string of 8 alphanumeric characters.
        """
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    @staticmethod
    def generate_db_username():
        """
        Generate a random database username.

        :return: A random string of 6 alphanumeric characters.
        """
        return ''.join(random.choices(string.ascii_lowercase, k=6))

    @staticmethod
    def generate_random_password(length=12):
        """
        Generate a secure random password.

        :param length: The length of the password (default is 12).
        :return: A random string of specified length containing letters, digits, and symbols.
        """
        characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
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


