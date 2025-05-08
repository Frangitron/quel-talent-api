from queltalentapi.components.authorization.abstract import AbstractAuthorization
from queltalentapi.components.http.abstract import AbstractHttp
from queltalentapi.components.http.user_claims import UserClaims
from queltalentapi.foundation.abstract_domain_component import AbstractDomainComponent
from queltalentapi.foundation.injector import Injector


class ProjectDomainComponent(AbstractDomainComponent):

    def __init__(self):
        self._http = Injector().inject(AbstractHttp)
        self._authorization = Injector().inject(AbstractAuthorization)

    def register_http_routes(self):
        self._http.register_route(path='/projects', method='get', callback=self.get_all)
        self._http.register_route(path='/projects/{id}', method='get', callback=self.get_by_id)

    async def get_by_id(
        self,
        id: str,
        user_claims: UserClaims
    ) -> list[str | UserClaims]:
        return ['PROJ', user_claims, id]

    async def get_all(
        self,
        user_claims: UserClaims
    ) -> list[str | UserClaims]:
        return ['coucou', 'caca', user_claims]
