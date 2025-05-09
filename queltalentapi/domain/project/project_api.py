from queltalentapi.domain.project.models import ProjectModel, ProjectResponseModel
from queltalentapi.foundation.injector import Injector
from queltalentapi.domain.project.database.abstract import AbstractProjectDatabase


def create(project: ProjectModel) -> ProjectResponseModel:
    database = Injector().inject(AbstractProjectDatabase)
    return database.create(project)


def delete(project_index: int) -> None:
    database = Injector().inject(AbstractProjectDatabase)
    database.delete(project_index)


def  get_all() -> list[ProjectResponseModel]:
    database = Injector().inject(AbstractProjectDatabase)
    return database.get_all()


def get_by_id(index: int) -> ProjectResponseModel:
    database = Injector().inject(AbstractProjectDatabase)
    return database.get_by_id(index)


def update(project: ProjectResponseModel) -> ProjectResponseModel:
    database = Injector().inject(AbstractProjectDatabase)
    return database.update(project)
