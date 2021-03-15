import logging

from fastapi import APIRouter, HTTPException

from koala.modules.common import Common
from koala.modules.devices.curd.device import UserDevices
from koala.modules.devices.mapper.device import mapper_register_device
from koala.modules.devices.models.device import BaseUserDeviceModel

router = APIRouter()


@router.post("/register_device")
async def register_device(device_data: BaseUserDeviceModel):
    try:
        common = Common()
        user_id = await common.find_by_username(username=device_data.user_name)
        user_device_data = mapper_register_device(
            device_data=device_data, user_id=user_id.get("_id")
        )

        user_devices = UserDevices()
        result = await user_devices.insert_user_device(
            user_device_data=user_device_data
        )
        return result

    except Exception as e:
        logging.info(e)
        raise HTTPException(status_code=500, detail="Not able to register device")
