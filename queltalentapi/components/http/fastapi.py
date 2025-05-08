import logging
import os
from inspect import signature, Parameter
from typing import Annotated

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from queltalentapi.components.authorization.abstract import AbstractAuthorization
from queltalentapi.components.http.abstract import AbstractHttp
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

    def register_route(self, path:str , method:str, callback: callable):
        _logger.info(f"Registering HTTP route for path '{path}' and method '{method}'")

        callback_parameters = dict(signature(callback).parameters)
        callback_parameters['user_claims'] =  Parameter(
            'user_claims',
            Parameter.KEYWORD_ONLY,
            default=Depends(self._validate_token),
            annotation=UserClaims
        )

        async def _route(
            **kwargs,
        ):
            return await callback(**kwargs)

        _route.__signature__.replace(parameters=list(callback_parameters.values()))

        self.get_app().add_api_route(
            path=path,
            endpoint=route,
            methods=[method]
        )

    #
    # FastAPI specific
    def _validate_token(self, credentials: HTTPBearerAuthorizationCredentials) -> UserClaims:
        token = credentials.credentials if credentials else None
        try:
            user_claims = self._auth.validate_token(token)
            return user_claims
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

    def get_app(self) -> FastAPI:
        if self._app is None:
            raise Exception("FastAPIHttp is not bootstrapped yet")

        return self._app
