import logging
import os

from inspect import signature, Parameter
from typing import Annotated, Type

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from queltalentapi.components.authorization.abstract import AbstractAuthorization
from queltalentapi.components.http.abstract import AbstractHttp
from queltalentapi.components.http.abstract_route import AbstractHttpRoute
from queltalentapi.components.http.user_claims import UserClaims
from queltalentapi.foundation.injector import Injector


_logger = logging.getLogger(__name__)

_security = HTTPBearer(auto_error=False)
HTTPBearerAuthorizationCredentials = Annotated[HTTPAuthorizationCredentials, Depends(_security)]


class FastApiHttp(AbstractHttp):
    def __init__(self):
        self._app: FastAPI | None = None
        self._auth : AbstractAuthorization | None = None

    def bootstrap(self):
        if os.environ.get("DEV"):
            self._app = FastAPI(root_path="/api/v1")
        else:
            self._app = FastAPI(root_path="/api/v1", docs_url=None, redoc_url=None)

        self._auth = Injector().inject(AbstractAuthorization)

    def register_route(self, route_type: Type[AbstractHttpRoute]):
        details = route_type.get_details()
        _logger.info(f"Registering HTTP route for path '{details.path}' and method '{details.method}'")

        route = route_type()
        async def endpoint_wrapper(user_claims: UserClaims = Depends(self._validate_token), **kwargs):
            route.user_claims = user_claims
            try:
                return await route.endpoint(**kwargs)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        parameters = dict(signature(route.callback).parameters)
        parameters['user_claims'] = Parameter(
            'user_claims',
            Parameter.KEYWORD_ONLY,
            default=Depends(self._validate_token),
            annotation=UserClaims
        )
        endpoint_wrapper.__signature__ = signature(endpoint_wrapper).replace(parameters=list(parameters.values()))

        self.get_app().add_api_route(
            path=details.path,
            endpoint=endpoint_wrapper,
            methods=[details.method]
        )

    #
    # FastAPI specific
    def _validate_token(self, credentials: HTTPBearerAuthorizationCredentials) -> UserClaims:
        token = credentials.credentials if credentials else None
        try:
            user_claims = self._auth.get_user_claims(token)
            return user_claims
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

    def get_app(self) -> FastAPI:
        if self._app is None:
            raise Exception("FastAPIHttp is not bootstrapped yet")

        return self._app
