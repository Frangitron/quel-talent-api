from queltalentapi.domain.project.database.abstract import AbstractProjectDatabase
from queltalentapi.domain.project.models import ProjectModel, ProjectResponseModel
from queltalentapi.foundation.event_bus.abstract import AbstractEventBus
from queltalentapi.foundation.event_bus.type_enum import EventBusEventType
from queltalentapi.foundation.injector import Injector


def create(project: ProjectModel) -> ProjectResponseModel:
    database = Injector().inject(AbstractProjectDatabase)
    new_record = database.create(project)

    event_bus = Injector().inject(AbstractEventBus)
    event_bus.publish(
        event_type=EventBusEventType.Create,
        event_data={
            "resource": "project",
            "data": new_record.model_dump()
        },
    )

    return new_record


def delete(project_index: int) -> None:
    database = Injector().inject(AbstractProjectDatabase)
    database.delete(project_index)

    event_bus = Injector().inject(AbstractEventBus)
    event_bus.publish(
        event_type=EventBusEventType.Delete,
        event_data={
            "resource": "project",
            "data": {"id": project_index}
        },
    )


def get_all() -> list[ProjectResponseModel]:
    database = Injector().inject(AbstractProjectDatabase)
    return database.get_all()


def get_by_id(index: int) -> ProjectResponseModel:
    database = Injector().inject(AbstractProjectDatabase)
    return database.get_by_id(index)


def update(project: ProjectResponseModel) -> ProjectResponseModel:
    database = Injector().inject(AbstractProjectDatabase)
    updated_record = database.update(project)

    event_bus = Injector().inject(AbstractEventBus)
    event_bus.publish(
        event_type=EventBusEventType.Update,
        event_data={
            "resource": "project",
            "data": updated_record.model_dump()
        },
    )

    return updated_record
