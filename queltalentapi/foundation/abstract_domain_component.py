from abc import ABC, abstractmethod


class AbstractDomainComponent(ABC):

    @abstractmethod
    def register_http_routes(self):
        pass
