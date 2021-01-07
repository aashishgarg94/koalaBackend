from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel

from koala.core.mongo_model import OID


class BaseOTPModel(BaseModel):
    phone_number: str
    generated_otp: int
    is_consumed: bool
    is_expired: bool


class OTPInModel(BaseOTPModel):
    expired_at: Optional[datetime]
    consumed_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class OTPOutModel(OTPInModel):
    id: OID = Field(..., alias="_id")
