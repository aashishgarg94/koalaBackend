from typing import Optional, TypeVar

from pydantic import BaseModel, EmailStr, SecretStr


# TODO: User role may need to be added over here
class UserModal(BaseModel):
    user_name: str
    email: EmailStr
    mobile_number: int
    disabled: Optional[bool] = False


class UserCreateModal(UserModal):
    email: EmailStr
    password: SecretStr


class UserUpdateModal(UserModal):
    password: SecretStr


class UserInDB(UserModal):
    hashed_password: str


class UserDB(BaseModel):
    user_name: str
    email: EmailStr
    mobile_number: int
    disabled: bool
    hashed_password: str

    class Config:
        orm_mode = True


UD = TypeVar("UD", bound=UserDB)
