from typing import List, Optional, TypeVar

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


class UserProof(BaseModel):
    name: Optional[str] = None
    is_uploaded: Optional[bool] = False


class UserBioModal(BaseModel):
    experience: Optional[int] = 0
    expected_salary: Optional[int] = 0
    current_salary: Optional[int] = 0
    previous_worked_area: Optional[List[str]] = None
    id_proof: UserProof
    address_proof: UserProof
    other_documents_needed: List[UserProof]
    is_resume_uploaded: bool = False


class UserModalNew(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    mobile_number: int
    disabled: Optional[bool] = False
    hashed_password: str
    bio: Optional[List[UserBioModal]] = None
