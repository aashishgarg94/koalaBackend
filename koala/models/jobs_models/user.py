from datetime import datetime
from typing import List, Optional, TypeVar

from koala.core.mongo_model import OID, MongoModel
from koala.models.jobs_models.master import BaseKeyValueModel, BaseRangeModel
from pydantic import BaseModel, EmailStr, Field, SecretStr

from ..social.users import FollowerModel
from .job_user import UserJobsRelationModel


class BaseFullNameModel(BaseModel):
    first_name: str
    middle_name: Optional[str] = ""
    last_name: Optional[str] = ""


class GpsModel(BaseModel):
    latitude: float
    longitude: float


# TODO: User role may need to be added over here

# Will try to get it either using GPS or fields, needs to decide later, keeping it alive for now
class UserModel(BaseModel):
    username: str
    full_name: BaseFullNameModel
    email: Optional[EmailStr]
    mobile_number: int
    gender: str
    current_city: Optional[str] = None
    current_area: Optional[str] = None
    current_gigtype: Optional[str] = None
    gps: Optional[GpsModel] = None


class UserRegisterModel(UserModel):
    password: SecretStr


class UserProof(BaseModel):
    name: Optional[str] = None
    is_uploaded: Optional[bool] = False


class BaseWorkHistoryModel(BaseModel):
    company_name: str
    title: str
    from_year: int
    to_year: int
    role: str


class BaseQualificationModel(BaseModel):
    level: str
    year: int
    institute: str


# NOTE: Created bio so on first iteration we don't have to MINE the complete user object
class UserBioModel(BaseModel):
    qualifications: Optional[List[BaseQualificationModel]]
    experience: float
    work_history: Optional[List[BaseWorkHistoryModel]]
    current_company: str = None
    current_salary: Optional[BaseRangeModel]
    expected_salary: Optional[BaseRangeModel]
    preferred_city: Optional[str]
    preferred_area: Optional[str]
    preferred_gigtype: Optional[str]
    job_preference: Optional[List[str]]  # Will create the options for this on frontend
    job_types: Optional[List[BaseKeyValueModel]]
    previous_worked_area: Optional[List[str]] = None
    id_proof: UserProof
    address_proof: UserProof
    other_documents: Optional[List[UserProof]]
    is_resume_uploaded: bool = False


class UserInModel(UserModel):
    hashed_password: str
    is_disabled: Optional[bool] = False
    is_updated: Optional[bool] = False
    is_deleted: Optional[bool] = False
    groups_followed: Optional[List[OID]] = []
    users_followed: Optional[List[OID]] = []  # Users followed by this user
    users_following: Optional[FollowerModel]  # Users following this user
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    disabled_on: Optional[datetime]
    deleted_on: Optional[datetime]
    bio: Optional[UserBioModel] = None
    job_applied: Optional[List[UserJobsRelationModel]] = []

    class Config:
        orm_mode = True


UD = TypeVar("UD", bound=UserInModel)


class UserOutModel(UserInModel, MongoModel):
    id: OID = Field()


class UserUpdateModel(MongoModel):
    full_name: Optional[BaseFullNameModel]
    mobile_number: Optional[int]


class UserUpdateCls(UserUpdateModel):
    username: Optional[str]
    is_updated: Optional[bool] = True
    is_disabled: Optional[bool] = False
    is_deleted: Optional[bool] = False
    updated_on: Optional[datetime] = datetime.now()
    disabled_on: Optional[datetime] = datetime.now()
    deleted_on: Optional[datetime] = datetime.now()


class UserUpdateOutModel(UserUpdateCls):
    id: OID = Field()


class BioUpdateInModel(UserBioModel):
    updated_on: Optional[datetime] = None


class BioUpdateOutModel(BioUpdateInModel, MongoModel):
    id: OID = Field()
