import logging
from abc import ABCMeta


_logger = logging.getLogger(__name__)


class MetaRoute(ABCMeta):

    routes = list()  # FIXME type hint is missing, fix circular deps

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        if bases:
            _logger.info(f"Subscribing HTTP route '{cls.__name__}' for registration")
            if attrs.get('details') is None:
                raise NotImplementedError(f"Route details are not set for route '{cls.__name__}'")

            MetaRoute.routes.append(cls)

        return cls
