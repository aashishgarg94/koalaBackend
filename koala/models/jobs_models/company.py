from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class BaseCompanyBenefits(BaseModel):
    name: str


class BaseCompanyBenefitsList(BaseModel):
    benefits: List[BaseCompanyBenefits]


class BaseCompanyRating(BaseModel):
    review_date: date
    rating: List[int]
    comments: List[str]
    comments_by_user_name: str
    comments_by_user_email: EmailStr


class BaseCompanyMoreInfo(BaseModel):
    about: Optional[str] = None
    reviews: Optional[BaseCompanyRating] = None


class BaseCompany(BaseModel):
    name: str
    logo: Optional[str]
    address_1: str
    address_2: Optional[str]
    city: str
    State: str
    pin_code: int
    benefits: Optional[BaseCompanyBenefitsList] = None
    more_info: Optional[BaseCompanyMoreInfo] = None


# Company jobs applied classes also needs to be created
