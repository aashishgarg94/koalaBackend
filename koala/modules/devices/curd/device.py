import logging

from koala.dao.mongo_base import MongoBase
from koala.config.collections import DEVICES
from koala.modules.devices.models.device import DeviceInModel, DeviceIdOutModel
from bson import ObjectId


class UserDevices:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(DEVICES)

    async def insert_user_device(self, user_device_data: DeviceInModel) -> any:
        try:
            # TODO: Also need to push user_id
            finder = {"device_id": user_device_data.device_id}
            user_device_data_dict = user_device_data.dict()
            user_device_data_dict["user_id"] = ObjectId(
                user_device_data_dict.get("user_id")
            )
            updater = {"$set": user_device_data.dict()}
            projection = {"_id": 1}

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

    async def get_fcm_tokens(self, user_ids: list) -> any:
        try:
            finder = {"_id": {"$in": user_ids}}
            projection = {"fcm_token": 1}

            result = await self.collection.find_one(
                finder=finder,
                projection=projection,
            )
            return result
        except Exception as e:
            logging.error(f"Error: while saving device details - {e}")
