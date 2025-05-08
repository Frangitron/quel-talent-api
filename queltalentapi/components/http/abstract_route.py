from dataclasses import dataclass
from abc import ABC, abstractmethod

from queltalentapi.components.http.user_claims import UserClaims


@dataclass()
class RouteDetails:
    path: str
    method: str


class AbstractHttpRoute(ABC):

    def __init__(self):
        self.user_claims: UserClaims | None = None

    @staticmethod
    @abstractmethod
    def get_details() -> RouteDetails:
        pass

    async def endpoint(self, **kwargs):
        self._validate()
        return await self.callback(**kwargs)

    @abstractmethod
    async def callback(self, **kwargs):
        pass

    def _validate(self):
        if self.user_claims is None:
            raise Exception("User claims are not set")
