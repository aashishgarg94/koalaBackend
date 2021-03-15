import logging

from koala.constants import REQUEST_SKIP_DEFAULT, REQUEST_LIMIT
from koala.dao.mongo_base import MongoBase
from koala.config.collections import DEVICES
from koala.modules.devices.models.device import DeviceInModel, DeviceIdOutModel


class UserDevices:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(DEVICES)

    async def insert_user_device(self, user_device_data: DeviceInModel) -> any:
        try:
            # TODO: Also need to push user_id
            finder = {
                "user_id": user_device_data.user_id,
                "device_id": user_device_data.device_id,
                "fcm_token": user_device_data.fcm_token,
            }

            user_device_data.dict()
            # user_device_data_dict["user_id"] = ObjectId(
            #     user_device_data_dict.get("user_id")
            # )
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
            finder = {"user_id": {"$in": user_ids}}
            projection = {"fcm_token": 1, "_id": 0}

            result = await self.collection.find(
                finder=finder,
                projection=projection,
                skip=REQUEST_SKIP_DEFAULT,
                limit=REQUEST_LIMIT,
            )

            fcm_list = []
            for fcm in await result.to_list(length=REQUEST_LIMIT):
                fcm_list.append(fcm.get("fcm_token"))

            return fcm_list
        except Exception as e:
            logging.error(f"Error: while saving device details - {e}")
