from queltalentapi.domain.project.database.abstract import AbstractProjectDatabase
from queltalentapi.domain.project.database.record import ProjectDatabaseRecord


class AlembicProjectDatabase(AbstractProjectDatabase):

    def get_all(self) -> list[ProjectDatabaseRecord]:
        return []
