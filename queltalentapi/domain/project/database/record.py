from pydantic import BaseModel


class ProjectDatabaseRecord(BaseModel):
    id: int
    name: str
