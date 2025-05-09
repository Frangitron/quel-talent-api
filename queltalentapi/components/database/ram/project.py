from httpapifoundation.exceptions import NotFoundError

from queltalentapi.domain.project.database.abstract import AbstractProjectDatabase
from queltalentapi.domain.project.models import ProjectModel, ProjectResponseModel


class RamProjectDatabase(AbstractProjectDatabase):
    """
    RAM implementation of the project database.
    """

    def __init__(self):
        self._data: dict[int: ProjectResponseModel] = dict()

    def create(self, project: ProjectModel) -> ProjectResponseModel:
        new_index = len(self._data)
        new_record = ProjectResponseModel(
            id=new_index,
            name=project.name,
        )
        self._data[new_index] = new_record
        return new_record

    def delete(self, project_index: int) -> None:
        try:
            self._data.pop(project_index)
        except KeyError:
            raise NotFoundError(f"Project with id {project_index} not found")

    def get_all(self) -> list[ProjectResponseModel]:
        return list(self._data.values())

    def get_by_id(self, index: int) -> ProjectResponseModel:
        try:
            return self._data[index]
        except KeyError:
            raise NotFoundError(f"Project with id {index} not found")

    def update(self, project: ProjectResponseModel) -> ProjectResponseModel:
        try:
            self._data[project.id] = project
            return project
        except KeyError:
            raise NotFoundError(f"Project with id {project.id} not found")
