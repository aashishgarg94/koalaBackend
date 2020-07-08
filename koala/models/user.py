from pydantic import BaseModel


class UserInDB(BaseModel):
    name: str = "Not found"
