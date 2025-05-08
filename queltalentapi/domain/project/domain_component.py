from queltalentapi.components.http.abstract import AbstractHttp
from queltalentapi.components.http.abstract_route import AbstractHttpRoute, RouteDetails
from queltalentapi.foundation.abstract_domain_component import AbstractDomainComponent
from queltalentapi.foundation.injector import Injector


class ProjectDomainComponent(AbstractDomainComponent):

    def __init__(self):
        self._http = Injector().inject(AbstractHttp)

    def register_http_routes(self):
        self._http.register_route(ProjectByIdRoute)
        self._http.register_route(ProjectsRoute)


class ProjectByIdRoute(AbstractHttpRoute):

    @staticmethod
    def get_details() -> RouteDetails:
        return RouteDetails(
            path='/projects/{index}/{cluf}',
            method='get'
        )

    async def callback(self, index: str, cluf: int):
        return ['PROJ', self.user_claims, index, cluf]


class ProjectsRoute(AbstractHttpRoute):

    @staticmethod
    def get_details() -> RouteDetails:
        return RouteDetails(
            path='/projects',
            method='get'
        )

    async def callback(self):
        return ['ALL', self.user_claims]
