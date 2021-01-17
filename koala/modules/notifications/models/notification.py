from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel

from koala.core.mongo_model import OID


class BaseNotificationModel(BaseModel):
    user_id: str
    title: str
    message: str


class NotificationInModel(BaseNotificationModel):
    read_at: Optional[datetime]
    sent_at: Optional[datetime]


class NotificationOutModel(NotificationInModel):
    id: OID = Field(..., alias="_id")
