from queltalentapi.foundation.abstract_domain_component import AbstractDomainComponent


class DomainComponentsStore:
    def __init__(self):
        self.domain_components: list[AbstractDomainComponent] = list()

    def add(self, domain_component: AbstractDomainComponent):
        self.domain_components.append(domain_component)

    def get_all(self) -> list[AbstractDomainComponent]:
        return self.domain_components
