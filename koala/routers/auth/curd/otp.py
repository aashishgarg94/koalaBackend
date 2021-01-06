import logging

from koala.config.collections import OTP_GENERATION
from koala.crud.jobs_crud.mongo_base import MongoBase


class OTPGeneration:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(OTP_GENERATION)

    async def get_count(self) -> int:
        try:
            pass
        except Exception as e:
            logging.error(f"Error: Job count {e}")
            raise e
