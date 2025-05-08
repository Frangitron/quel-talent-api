from abc import ABC, abstractmethod
from typing import Type

from queltalentapi.components.http.abstract_route import AbstractHttpRoute


class AbstractHttp(ABC):

    @abstractmethod
    def bootstrap(self):
        pass

    @abstractmethod
    def register_route(self, route_type: Type[AbstractHttpRoute]):
        pass
