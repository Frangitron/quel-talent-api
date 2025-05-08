import logging
logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv
load_dotenv('resources/.env')

from queltalentapi.components.authorization.abstract import AbstractAuthorization
from queltalentapi.components.bootstrapper import Bootstrapper
from queltalentapi.components.http.abstract import AbstractHttp
from queltalentapi.domain.project.database.abstract import AbstractProjectDatabase
from queltalentapi.foundation.domain_components_store import DomainComponentsStore
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
        DomainComponentsStore: DomainComponentsStore(),
    })


def _register_domain_components():
    from queltalentapi.domain.project.domain_component import ProjectDomainComponent

    store = Injector().inject(DomainComponentsStore)
    store.add(ProjectDomainComponent())


_register_dependencies()
_register_domain_components()
bootstrapper = Bootstrapper()
bootstrapper.bootstrap()

# FastAPI specific
app = Injector().inject(AbstractHttp).get_app()
