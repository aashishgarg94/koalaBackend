import logging

from koala.dao.mongo_base import MongoBase
from koala.config.collections import DEVICES
from koala.modules.devices.models.device import DeviceInModel, DeviceIdOutModel


class UserDevices:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(DEVICES)

    async def insert_user_device(self, device_data: DeviceInModel) -> any:
        try:
            finder = {"device_id": device_data.device_id}
            updater = {
                "$set": device_data.dict()
            }
            projection = {'_id': True}

            result = await self.collection.find_one_and_modify(
                finder=finder,
                update=updater,
                projection=projection,
                upsert=True,
                return_updated_document=True,
            )
            return DeviceIdOutModel(id=result.get("_id"))
        except Exception as e:
            logging.error(f"Error: while saving device details - {e}")
