from queltalentapi.components.http.abstract_route import AbstractHttpRoute, RouteDetails


class ProjectByIdRoute(AbstractHttpRoute):
    details = RouteDetails(
            path='/projects/{index}/{cluf}',
            method='get'
        )

    async def callback(self, index: str, cluf: int):
        return ['PROJ', self.user_claims, index, cluf]


class ProjectsRoute(AbstractHttpRoute):
    details = RouteDetails(
            path='/projects',
            method='get'
        )

    async def callback(self):
        return ['ALL', self.user_claims]
