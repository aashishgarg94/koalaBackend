import logging
from datetime import datetime

from koala.dao.mongo_base import MongoBase
from koala.modules.otp.mapper.otp import mapper_save_otp
from koala.config.collections import OTP_GENERATION
from koala.modules.otp.models.otp import OTPInModel


class OTP:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(OTP_GENERATION)

    async def save_by_phone_number(self, phone_number: str, verify_code: int) -> any:
        try:
            otp_model: OTPInModel = mapper_save_otp(
                phone_number=phone_number, verify_code=verify_code
            )

            result = await self.collection.insert_one(document=otp_model.dict())

            return (
                {"status_code": 200, "data": {"is_generated": False}}
                if result
                else {"status_code": 500, "error": {"msg": "Not able to save OTP"}}
            )
        except Exception as e:
            logging.error(f"Error: while saving OTP {e}")

    async def get_by_phone_number(self, phone_number: str) -> any:
        try:
            filter_condition = {
                "$query": {
                    "phone_number": phone_number,
                    "is_consumed": False,
                    "is_expired": False,
                },
                "$orderby": {"created_at": -1},
            }

            result = await self.collection.find_one(
                finder=filter_condition,
                projection={"generated_otp": 1, "expired_at": 1},
            )

            return result
        except Exception as e:
            logging.error(f"Error: while saving OTP {e}")

    async def update_by_phone_number(self, phone_number: str) -> any:
        try:
            finder = {"phone_number": phone_number}
            updater = {
                "$set": {
                    "is_consumed": True,
                    "consumed_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            }
            sort = [("created_at", -1)]

            return await self.collection.find_one_and_modify(
                finder=finder,
                update=updater,
                sort=sort,
                return_updated_document=False,
            )
        except Exception as e:
            logging.error(f"Error: while saving OTP - {e}")
