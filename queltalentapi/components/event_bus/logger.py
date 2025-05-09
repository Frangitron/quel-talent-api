import logging

from queltalentapi.foundation.event_bus.abstract import AbstractEventBus


_logger = logging.getLogger("EventBus")


class LoggerEventBus(AbstractEventBus):

    def publish(self, event_type: str, event_data: dict):
        _logger.info(event_type)
        _logger.info(event_data)
