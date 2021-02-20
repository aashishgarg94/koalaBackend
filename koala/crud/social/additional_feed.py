import logging
from bson import ObjectId
from fastapi import HTTPException
from koala.models.jobs_models.master import BaseIsCreated
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.config.collections import ADDITIONAL_FEED
from koala.models.social.users import (
    CreateAdditionalFeedModelOut
)

class AdditionalFeedCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(ADDITIONAL_FEED)

    async def get_all_feed(self) -> any:
        try:
            filter_condition = {"is_deleted": False}
            data = await self.collection.find(
                finder=filter_condition,
                return_doc_id=True,
                extended_class_model=CreateAdditionalFeedModelOut
            )

            return data if data else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
