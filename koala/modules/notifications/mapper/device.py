from datetime import datetime

from koala.modules.notifications.models.device import BaseDeviceModel, DeviceInModel


def mapper_register_device(device_data: BaseDeviceModel):
    in_device_data = DeviceInModel(**device_data.dict())
    in_device_data.is_active = True
    in_device_data.created_at = datetime.now()
    in_device_data.disabled_at = datetime.now()
    return in_device_data
