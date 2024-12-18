import logging
from abc import ABC, abstractmethod

class BaseHandler(ABC):
    def __init__(self):
        self.next_handler = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def set_next(self, handler):
        self.logger.info(f"Setting next handler: {handler.__class__.__name__}")
        self.next_handler = handler
        return handler

    def handle(self, context=None, *args, **kwargs):
        if context is None:
            context = {}
        else:
            self.logger.info(f"Received context in handler {self.__class__.__name__}")
            #debug
            self.logger.debug(context)
        self.logger.info(f"Handling request in {self.__class__.__name__}")
        try:
            result = self.process(context, *args, **kwargs)  # Pass the shared context
        except Exception as e:
            self.logger.error(f"Error in handler {self.__class__.__name__}: {e}", exc_info=True)
            raise

        if result is not None:  # If result is returned, terminate the chain
            self.logger.info(f"Handler {self.__class__.__name__} processed the request.")
            return result

        if self.next_handler:
            self.logger.info(f"Passing request to next handler: {self.next_handler.__class__.__name__}")
            return self.next_handler.handle(context, *args, **kwargs)  # Pass the shared context to the next handler

        self.logger.warning(f"End of chain reached. No handler could process the request.")
        return None

    @abstractmethod
    def process(self, context, *args, **kwargs):
        pass

