from fastapi import HTTPException
from koala.models.jobs_models.master import BaseIsCreated
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.config.collections import VIDEOS_WATCHED
from koala.models.learning.learning import CreateVideoWatchedModelIn


class VideosWatchedCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(VIDEOS_WATCHED)

    async def video_watched_action(
        self, video_watched_details: CreateVideoWatchedModelIn
    ) -> any:
        try:
            insert_id = await self.collection.insert_one(
                video_watched_details.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )

            return BaseIsCreated(id=insert_id, is_created=True) if insert_id else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
