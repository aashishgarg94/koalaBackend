import logging
import datetime
from bson import ObjectId
from fastapi import HTTPException
from koala.models.jobs_models.master import BaseIsCreated, BaseIsUpdated
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.config.collections import STREAKS
from koala.models.social.users import (
    CreateStreakModelOut
)

class StreaksCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(STREAKS)

    async def video_streak(
        self,
        video_id: str,
        user_id: str,
        started: int = None,
        finished: int = None
    ) -> any:
        try:
            data = await self.collection.find_one(
                finder={"streak_type": "Video Started", "user_id": user_id},
                return_doc_id=True,
                extended_class_model=CreateStreakModelOut,
            )

            if data is not None:
                
                date_limit = data.last_update + datetime.timedelta(days=1)
                valid_streak = datetime.datetime.now().date() <= date_limit.date()
                finder = {"_id": ObjectId(data.id)}
                
                if valid_streak:
                    streak_increased = data.last_update.date() < datetime.datetime.now().date()
                    if streak_increased:
                        updater = {
                            "$inc": {"current_streak": 1},
                            "$set": {"last_update": datetime.datetime.now()}
                        }

                        result = await self.collection.find_one_and_modify(
                            find=finder,
                            update=updater,
                            return_doc_id=True,
                            return_updated_document=True,
                            extended_class_model=CreateStreakModelOut,
                        )

                        return BaseIsUpdated(id=result.id, is_updated=True) if result else None

                else:
                    updater = {
                        "$set": {"current_streak": 1, "last_update": datetime.datetime.now()},
                        "$push": {
                            "prev_streaks": {
                                "streak_length": data.current_streak,
                                "streak_end": datetime.datetime.now()
                            }
                        }
                    }

                    result = await self.collection.find_one_and_modify(
                        find=finder,
                        update=updater,
                        return_doc_id=True,
                        return_updated_document=True,
                        extended_class_model=CreateStreakModelOut,
                    )

                    return BaseIsUpdated(id=result.id, is_updated=True) if result else None

            else:
                video_streak_create = {
                    "streak_type": "Video Started",
                    "user_id": user_id,
                    "current_streak": 1,
                    "last_update": datetime.datetime.now(),
                    "prev_streaks": []
                }
                insert_id = await self.collection.insert_one(
                    video_streak_create,
                    return_doc_id=True,
                    extended_class_model=BaseIsCreated,
                )

                return BaseIsCreated(id=insert_id, is_created=True) if insert_id else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")