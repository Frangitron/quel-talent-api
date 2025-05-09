import logging
import os

from inspect import signature, Parameter
from typing import Annotated, Type

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from queltalentapi.foundation.authorization.abstract import AbstractAuthorization
from queltalentapi.foundation.http.abstract import AbstractHttp
from queltalentapi.foundation.http.abstract_route import AbstractHttpRoute
from queltalentapi.foundation.http.exception_handler import handle_exceptions
from queltalentapi.foundation.http.user_claims import UserClaims
from queltalentapi.foundation.injector import Injector


_logger = logging.getLogger(__name__)

_security = HTTPBearer(auto_error=False)
HTTPBearerAuthorizationCredentials = Annotated[HTTPAuthorizationCredentials, Depends(_security)]


class FastApiHttp(AbstractHttp):
    def __init__(self):
        super().__init__()
        self._app: FastAPI | None = None
        self._auth : AbstractAuthorization | None = None

    def bootstrap(self):
        if os.environ.get("DEV"):
            self._app = FastAPI(root_path="/api/v1")
        else:
            self._app = FastAPI(root_path="/api/v1", docs_url=None, redoc_url=None)

        self._auth = Injector().inject(AbstractAuthorization)

    def register_route(self, route_type: Type[AbstractHttpRoute]):

        async def endpoint_wrapper(user_claims: UserClaims = Depends(self._get_user_claims), **kwargs):
            route = route_type()
            route.user_claims = user_claims
            return await handle_exceptions(route.endpoint, **kwargs)

        parameters = dict(signature(route_type.callback).parameters)
        parameters.pop('self')
        parameters['user_claims'] = Parameter(
            'user_claims',
            Parameter.KEYWORD_ONLY,
            default=Depends(self._get_user_claims),
            annotation=UserClaims
        )
        endpoint_wrapper.__signature__ = signature(endpoint_wrapper).replace(parameters=list(parameters.values()))
        endpoint_wrapper.__doc__ = route_type.__doc__

        self.get_app().add_api_route(
            endpoint=endpoint_wrapper,
            methods=[route_type.details.method.value],
            name=route_type.details.name,
            operation_id=route_type.details.operation_id,
            path=route_type.details.path,
        )

    def get_app(self) -> FastAPI:
        if self._app is None:
            raise Exception("FastAPIHttp is not bootstrapped yet")

        return self._app

    def _get_user_claims(self, credentials: HTTPBearerAuthorizationCredentials) -> UserClaims:
        token = credentials.credentials if credentials else None
        try:
            user_claims = self._auth.get_user_claims(token)
            return user_claims
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
