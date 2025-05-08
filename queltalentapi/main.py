import logging
logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv
load_dotenv('resources/.env')

from queltalentapi.components.bootstrapper import Bootstrapper
from queltalentapi.domain.project.database.abstract import AbstractProjectDatabase
from queltalentapi.foundation.authorization.abstract import AbstractAuthorization
from queltalentapi.foundation.http.abstract import AbstractHttp
from queltalentapi.foundation.injector import Injector


def _register_dependencies():
    # from queltalentapi.components.authorization.auth0 import Auth0Authorization
    from queltalentapi.components.authorization.noauth import NoAuthorization
    from queltalentapi.components.http.fastapi import FastApiHttp
    from queltalentapi.domain.project.database.alembic.implementation import AlembicProjectDatabase

    Injector().set_dependencies({
        AbstractAuthorization: NoAuthorization(),
        AbstractHttp: FastApiHttp(),
        AbstractProjectDatabase: AlembicProjectDatabase(),
    })


def _import_routes():
    from queltalentapi.domain.project import routes


_register_dependencies()
_import_routes()
bootstrapper = Bootstrapper()
bootstrapper.bootstrap()

# FastAPI specific
app = Injector().inject(AbstractHttp).get_app()
