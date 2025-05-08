from abc import ABC, abstractmethod

from queltalentapi.components.http.user_claims import UserClaims


class AbstractHttp(ABC):

    @abstractmethod
    def bootstrap(self):
        pass

    @abstractmethod
    def register_route(self, path:str , method:str, callback: callable):
        pass
