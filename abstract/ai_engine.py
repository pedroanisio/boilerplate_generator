import logging
from abc import ABC, abstractmethod

class AbstractAIEngine(ABC):
    """
    Abstract base class for an Engine that completes tasks given a Flavor.
    """
    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        self.logger.debug("Initializing AbstractAIEngine")

    @abstractmethod
    def complete(self, flavor) -> str:
        """
        Abstract method for completing a task based on the given flavor.

        :param flavor: An object containing system and user messages.
        :return: The completion result from the chat model.
        """
        pass
