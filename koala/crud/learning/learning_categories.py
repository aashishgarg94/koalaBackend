from bson import ObjectId
from fastapi import HTTPException
from koala.config.collections import LEARNING_CATEGORIES
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.learning.learning import (
    CreateLearningCategoriesModelIn,
    CreateLearningCategoriesModelOut,
)


class LearningCategoriesCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(LEARNING_CATEGORIES)

    async def create_learning_category(
        self, category_details: CreateLearningCategoriesModelIn
    ) -> any:
        try:
            insert_id = await self.collection.insert_one(
                category_details.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )

            return BaseIsCreated(id=insert_id, is_created=True) if insert_id else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_learning_category(
        self, category_id: str, title: str, image: str
    ) -> any:
        try:
            category_updates = {}
            if title is not None:
                category_updates["title"] = title.strip()
            if image is not None:
                category_updates["image"] = image.strip()

            finder = {"_id": ObjectId(category_id)}
            updater = {"$set": category_updates}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateLearningCategoriesModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_all_learning_categories(self) -> any:
        try:
            filter_condition = {"is_deleted": False}
            data = await self.collection.find(
                finder=filter_condition,
                return_doc_id=True,
                extended_class_model=CreateLearningCategoriesModelOut,
            )

            return data if data else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
