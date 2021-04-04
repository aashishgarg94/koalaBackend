import logging
from datetime import datetime

from bson import ObjectId
from fastapi import File, HTTPException, UploadFile
from koala.config.collections import SOCIAL_POSTS
from koala.dao.mongo_base import MongoBase
from koala.modules.social.posts.mapper.posts import (
    mapper_create_post,
    mapper_update_post,
)
from koala.modules.social.posts.models.posts import BasePostModel, BasePostUpdateModel
from koala.utils.utils import upload_social_post_image


class Posts:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(SOCIAL_POSTS)

    async def create_post(
        self,
        post_details: BasePostModel,
        file: UploadFile = File(...),
    ) -> any:
        try:
            s3_post_url = ""
            # Upload image to get S3 url
            if file is not None:
                post_image_upload_result = await upload_social_post_image(file=file)
                if post_image_upload_result.get("is_post_image_upload") is True:
                    s3_post_url = post_image_upload_result.get("post_image_url")

            post_data = mapper_create_post(
                post_details=post_details, media_url=s3_post_url
            )

            return await self.collection.insert_one(post_data.dict())
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_post(
        self,
        post_id: str,
        post_details: BasePostUpdateModel,
        file: UploadFile = File(...),
    ) -> any:
        try:
            s3_post_url = ""
            # Upload image to get S3 url
            if file is not None:
                post_image_upload_result = await upload_social_post_image(file=file)
                if post_image_upload_result.get("is_post_image_upload") is True:
                    s3_post_url = post_image_upload_result.get("post_image_url")

            post_data = mapper_update_post(
                post_details=post_details, media_url=s3_post_url
            )

            find = {"_id": ObjectId(post_id)}
            updater = {"$set": post_data.dict()}
            projection = {"_id": 1}
            return await self.collection.find_one_and_modify(
                find, update=updater, projection=projection
            )
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def disable_by_post_id(self, post_id: str) -> any:
        try:
            find = {"_id": ObjectId(post_id)}
            updater = {"$set": {"is_deleted": True, "deleted_at": datetime.now()}}
            projection = {"_id": 1}
            return await self.collection.find_one_and_modify(
                find, update=updater, projection=projection
            )
        except Exception as e:
            logging.error(f"Error: While deleting post {e}")
            raise e

    async def report_post(self, post_id: str) -> any:
        try:
            find = {"_id": ObjectId(post_id)}
            updater = {"$set": {"is_reported": True, "reported_at": datetime.now()}}
            projection = {"_id": 1}
            return await self.collection.find_one_and_modify(
                find, update=updater, projection=projection
            )
        except Exception as e:
            logging.error(f"Error: While deleting post {e}")
            raise e
