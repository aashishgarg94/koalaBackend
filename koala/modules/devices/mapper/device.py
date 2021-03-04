from datetime import datetime

from koala.core.mongo_model import OID
from koala.modules.devices.models.device import BaseDeviceModel, DeviceInModel


def mapper_register_device(device_data: BaseDeviceModel, user_id: OID):
    in_device_data = DeviceInModel(**device_data.dict(), user_id=user_id)
    in_device_data.is_active = True
    in_device_data.created_at = datetime.now()
    in_device_data.disabled_at = datetime.now()
    return in_device_data
