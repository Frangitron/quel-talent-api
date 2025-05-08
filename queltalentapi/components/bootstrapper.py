import logging

from queltalentapi.components.http.abstract import AbstractHttp
from queltalentapi.foundation.domain_components_store import DomainComponentsStore
from queltalentapi.foundation.injector import Injector


_logger = logging.getLogger(__name__)


class Bootstrapper:
    def __init__(self):
        self.domain_components_store: DomainComponentsStore | None = None
        self.http: AbstractHttp | None = None

    def bootstrap(self):
        self.domain_components_store = Injector().inject(DomainComponentsStore)
        self.http = Injector().inject(AbstractHttp)
        self.http.bootstrap()
        self._register_http_routes()

    def _register_http_routes(self):
        for domain_component in self.domain_components_store.get_all():
            _logger.info(f"Registering HTTP routes for domain component '{domain_component.__class__.__name__}'")
            domain_component.register_http_routes()
