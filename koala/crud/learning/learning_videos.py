import logging
from bson import ObjectId
from fastapi import HTTPException
from koala.config.collections import LEARNING_VIDEOS
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.learning.learning import (
    BaseLearningVideosModel,
    CreateLearningVideosModelIn,
    CreateLearningVideosModelOut,
    CreateLearningVideosModelOutList
)

class LearningVideosCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(LEARNING_VIDEOS)

    async def create_learning_video(
        self,
        video_details: CreateLearningVideosModelIn
    ) -> any:
        try:
            insert_id = await self.collection.insert_one(
                video_details.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )

            return BaseIsCreated(id=insert_id, is_created=True) if insert_id else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_learning_video(
        self,
        element_id: str,
        video_id: str,
        title: str,
        category: str,
        category_id: str,
        lesson_number: int,
        description: str,
        image: str
    ) -> any:
        try:
            video_updates = {}
            if title is not None:
                video_updates["title"] = title.strip()
            if category is not None:
                video_updates["category"] = category.strip()
            if category_id is not None:
                video_updates["category_id"] = category_id.strip()
            if lesson_number is not None:
                video_updates["lesson_number"] = lesson_number
            if lesson_number is not None:
                video_updates["video_id"] = video_id
            if description is not None:
                video_updates["description"] = description.strip()
            if image is not None:
                video_updates["image"] = image.strip()

            finder = {"_id": ObjectId(element_id)}
            updater = {"$set": video_updates}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateLearningVideosModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_all_learning_videos(
        self,
        category_id: str
    ) -> any:
        try:
            filter_condition = {"is_deleted": False, "category_id": category_id}
            data = await self.collection.find(
                finder=filter_condition,
                return_doc_id=True,
                extended_class_model=CreateLearningVideosModelOut,
            )

            return data if data else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
