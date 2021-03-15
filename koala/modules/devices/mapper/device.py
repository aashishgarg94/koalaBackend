from datetime import datetime

from koala.core.mongo_model import OID
from koala.modules.devices.models.device import BaseDeviceModel, DeviceInModel


def mapper_register_device(device_data: BaseDeviceModel, user_id: OID):
    return DeviceInModel(
        **device_data.dict(), user_id=user_id, created_at=datetime.now(), is_active=True
    )
