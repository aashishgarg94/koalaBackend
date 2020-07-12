from typing import Optional, TypeVar

from pydantic import BaseModel, EmailStr, SecretStr


# TODO: User role may need to be added over here
class UserModal(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    mobile_number: int
    disabled: Optional[bool] = False


class UserBasic(BaseModel):
    username: Optional[str]
    email: Optional[str]


class UserCreateModal(UserModal):
    email: EmailStr
    password: SecretStr


class UserUpdateCls(BaseModel):
    username: Optional[str]
    full_name: Optional[str]
    email: Optional[EmailStr]
    mobile_number: Optional[int]
    password: Optional[SecretStr]


class UserUpdateModal(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    mobile_number: Optional[int]
    password: Optional[SecretStr]


class UserDB(UserModal):
    hashed_password: str

    class Config:
        orm_mode = True


UD = TypeVar("UD", bound=UserDB)
