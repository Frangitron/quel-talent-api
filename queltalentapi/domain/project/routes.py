from httpapifoundation.http.abstract_route import AbstractHttpRoute
from httpapifoundation.http.route_details import RouteDetails
from httpapifoundation.http.method_enum import HttpMethod

from queltalentapi.domain.project import project_api
from queltalentapi.domain.project.models import ProjectModel, ProjectResponseModel


class ProjectCreateRoute(AbstractHttpRoute):
    """
    Creates a new Project.
    """
    details = RouteDetails(
        method=HttpMethod.POST,
        name='Create',
        operation_id='projects_Create',
        path='/projects',
    )

    async def callback(self, project: ProjectModel) -> ProjectResponseModel:
        return project_api.create(project)


class ProjectDeleteRoute(AbstractHttpRoute):
    """
    Deletes a Project.
    """
    details = RouteDetails(
        method=HttpMethod.DELETE,
        name='Delete',
        operation_id='projects_Delete',
        path='/projects/{index}',
    )

    async def callback(self, index: int) -> None:
        return project_api.delete(index)


class ProjectsAllRoute(AbstractHttpRoute):
    """
    Gets all Projects.
    """
    details = RouteDetails(
        method=HttpMethod.GET,
        name='Get all',
        operation_id='projects_GetAll',
        path='/projects',
    )

    async def callback(self) -> list[ProjectResponseModel]:
        return project_api.get_all()


class ProjectByIdRoute(AbstractHttpRoute):
    """
    Gets a Project by id.

    - **id**: integer
    """
    details = RouteDetails(
        method=HttpMethod.GET,
        name='Get by id',
        operation_id='project_GetById',
        path='/projects/{index}',
    )

    async def callback(self, index: int) -> ProjectResponseModel:
        return project_api.get_by_id(index)


class ProjectUpdateRoute(AbstractHttpRoute):
    """
    Updates a Project.
    """
    details = RouteDetails(
        method=HttpMethod.PUT,
        name='Update',
        operation_id='projects_Update',
        path='/projects',
    )

    async def callback(self, project: ProjectResponseModel) -> ProjectResponseModel:
        return project_api.update(project)
