from datetime import datetime
from typing import Optional

from pydantic import Field

from koala.core.mongo_model import OID, MongoModel


class BaseDeviceModel(MongoModel):
    device_id: str
    fcm_token: str


class BaseUserDeviceModel(BaseDeviceModel):
    user_name: str


class DeviceInModel(BaseDeviceModel):
    user_id: OID = Field()
    is_active: Optional[bool] = True
    created_at: Optional[datetime]
    disabled_at: Optional[datetime]


class DeviceIdOutModel(MongoModel):
    id: OID = Field()
