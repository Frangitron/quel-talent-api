from abc import ABC, abstractmethod

from queltalentapi.domain.project.models import ProjectModel, ProjectResponseModel


class AbstractProjectDatabase(ABC):

    @abstractmethod
    def create(self, project: ProjectModel) -> ProjectResponseModel:
        pass

    @abstractmethod
    def delete(self, project_index: int) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[ProjectResponseModel]:
        pass

    @abstractmethod
    def get_by_id(self, index: int) -> ProjectResponseModel:
        pass

    @abstractmethod
    def update(self, project: ProjectResponseModel) -> ProjectResponseModel:
        pass
