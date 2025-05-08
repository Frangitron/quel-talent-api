from pydantic import BaseModel


class UserClaims(BaseModel):
    name: str
