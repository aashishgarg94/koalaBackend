from fastapi import APIRouter, HTTPException

from koala.modules.devices.curd.device import UserDevices
from koala.modules.devices.mapper.device import mapper_register_device
from koala.modules.devices.models.device import BaseDeviceModel

router = APIRouter()


@router.post("/register_device")
async def register_device(device_data: BaseDeviceModel):
    try:
        device_data = mapper_register_device(device_data=device_data)

        user_devices = UserDevices()
        result = await user_devices.insert_user_device(device_data=device_data)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail="Not able to register device")
