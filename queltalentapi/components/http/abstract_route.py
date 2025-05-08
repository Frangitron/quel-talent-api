from abc import abstractmethod

from queltalentapi.components.http.meta_route import MetaRoute
from queltalentapi.components.http.route_details import RouteDetails
from queltalentapi.components.http.user_claims import UserClaims


class AbstractHttpRoute(metaclass=MetaRoute):

    details: RouteDetails | None = None

    def __init__(self):
        self.user_claims: UserClaims | None = None

    @abstractmethod
    async def callback(self, **kwargs):
        pass

    async def endpoint(self, **kwargs):
        self._validate()
        return await self.callback(**kwargs)

    def _validate(self):
        if self.user_claims is None:
            raise Exception("User claims are not set")
