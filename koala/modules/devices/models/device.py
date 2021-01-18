from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel

from koala.core.mongo_model import OID, MongoModel


class BaseDeviceModel(BaseModel):
    device_id: str
    fcm_token: str
    user_name: str


class DeviceInModel(BaseDeviceModel):
    is_active: Optional[bool] = True
    created_at: Optional[datetime]
    disabled_at: Optional[datetime]


class DeviceIdOutModel(MongoModel):
    id: OID = Field()
