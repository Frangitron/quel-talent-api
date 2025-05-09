from pydantic import BaseModel


class ProjectModel(BaseModel):
    name: str


class ProjectResponseModel(ProjectModel):
    id: int
