from abc import ABC, abstractmethod

from queltalentapi.domain.project.database.record import ProjectDatabaseRecord


class AbstractProjectDatabase(ABC):

    @abstractmethod
    def get_all(self) -> list[ProjectDatabaseRecord]:
        pass
