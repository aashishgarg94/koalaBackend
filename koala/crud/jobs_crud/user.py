import logging
from datetime import datetime
from typing import Optional, Type

from bson import ObjectId
from fastapi import HTTPException
from koala.config.collections import SOCIAL_POSTS, USERS
from koala.models.jobs_models.master import BaseIsCreated, BaseIsDisabled, BaseIsUpdated
from koala.models.jobs_models.user import (
    UD,
    BioUpdateInModel,
    BioUpdateOutModel,
    BioUpdateWithUserDetailOutModel,
    UserInModel,
    UserModel,
    UserOutModel,
    UserUpdateCls,
    UserUpdateOutModel,
)

from ..social.users import SocialPostsCollection
from .mongo_base import MongoBase, return_id_transformation


class MongoDBUserDatabase:
    def __init__(self, user_db_model: Type[UD]):
        self.user_db_model = user_db_model
        self.collection = MongoBase()
        self.collection(USERS)

    async def find_by_object_id(self, user_id: ObjectId) -> Optional[UD]:
        try:
            return await self.collection.find_one(
                {"_id": user_id},
                return_doc_id=True,
                extended_class_model=UserOutModel,
            )
        except Exception as e:
            raise e

    async def find_by_email(self, email: str) -> Optional[UD]:
        try:
            return await self.collection.find_one(
                {"email": email},
                return_doc_id=True,
                extended_class_model=UserOutModel,
            )
        except Exception as e:
            raise e

    async def find_by_username(self, username: str) -> Optional[UD]:
        try:
            return await self.collection.find_one(
                {"username": username},
                return_doc_id=True,
                extended_class_model=UserOutModel,
            )
        except Exception as e:
            raise e

    async def find_by_mobile_number(self, mobile_number: str) -> Optional[UD]:
        try:
            return await self.collection.find_one(
                {"mobile_number": mobile_number},
                return_doc_id=True,
                extended_class_model=UserOutModel,
            )
        except Exception as e:
            raise e

    # Not in use currently
    async def find_groups_followed_by_email(self, email: str) -> Optional[UD]:
        try:
            return await self.collection.find(
                finder={"email": email},
                projection={"groups_followed": 1, "_id": 0},
                return_doc_id=False,
            )
        except Exception as e:
            raise e

    async def find_groups_followed_by_username(self, username: str) -> Optional[UD]:
        try:
            return await self.collection.find(
                finder={"username": username},
                projection={"groups_followed": 1, "_id": 0},
                return_doc_id=False,
            )
        except Exception as e:
            raise e

    # Not in use currently
    async def find_user_followed_by_email(self, email: str) -> Optional[UD]:
        try:
            return await self.collection.find(
                finder={"email": email},
                projection={"users_followed": 1, "_id": 0},
                return_doc_id=False,
            )
        except Exception as e:
            raise e

    async def find_user_followed_by_username(self, username: str) -> Optional[UD]:
        try:
            return await self.collection.find(
                finder={"username": username},
                projection={"users_followed": 1, "_id": 0},
                return_doc_id=False,
            )
        except Exception as e:
            raise e

    async def create_user(self, user: UserInModel) -> BaseIsCreated:
        try:
            user.created_on = datetime.now()
            result = await self.collection.insert_one(
                user.dict(), return_doc_id=True, extended_class_model=BaseIsCreated
            )
            return BaseIsCreated(id=result, is_created=True) if result else None
        except Exception as e:
            raise e

    async def find_and_modify(
        self, user_update: UserUpdateCls, current_user: UserModel
    ) -> UserUpdateOutModel:
        try:
            find = {"username": current_user.username}
            user_update.is_updated = True
            user_update.updated_on = datetime.now()
            user = await self.collection.find_one_and_modify(
                find,
                {"$set": user_update.dict(exclude_unset=True)},
                return_doc_id=True,
                extended_class_model=UserUpdateOutModel,
            )
            return user if user else None
        except Exception as e:
            raise e

    async def disable_one(self, username: str) -> BaseIsDisabled:
        try:
            find = {"username": username}
            updater = {"$set": {"is_disabled": True, "disabled_on": datetime.now()}}
            # user.is_disabled = True
            # user.disabled_on = datetime.now()
            result = await self.collection.find_one_and_modify(
                find,
                update=updater,
                return_doc_id=True,
                extended_class_model=BaseIsDisabled,
            )
            data = result if result else None
            return data
        except Exception as e:
            raise e

    async def user_bio_update(
        self, bio_updates: BioUpdateInModel, current_user: UserModel
    ) -> BioUpdateOutModel:
        try:
            find = {"username": current_user.username}
            bio_updates.updated_on = datetime.now()
            result = await self.collection.find_one_and_modify(
                find,
                {"$set": {"bio": bio_updates.dict(exclude_unset=True)}},
            )

            custom_bio_dict = result.get("bio")
            custom_bio_dict["_id"] = result.get("_id")
            result_transformation = return_id_transformation(
                extended_class_model=BioUpdateOutModel, result=custom_bio_dict
            )

            return result_transformation if result else None
        except Exception as e:
            raise e

    async def user_bio_fetch(
        self, username: str, user_id: str = None
    ) -> Optional[BioUpdateWithUserDetailOutModel]:
        try:
            if user_id is None:
                result = await self.collection.find_one({"username": username})
            else:
                result = await self.collection.find_one({"_id": ObjectId(user_id)})

            if result.get("bio"):
                custom_bio_dict = result.get("bio")
                custom_bio_dict["_id"] = result.get("_id")
                custom_bio_dict["profile_image"] = result.get("profile_image")
                custom_bio_dict["name"] = result.get("full_name").get("first_name")
                result_transformation = return_id_transformation(
                    extended_class_model=BioUpdateWithUserDetailOutModel,
                    result=custom_bio_dict,
                )
                return result_transformation

            raise HTTPException(status_code=200, detail="Bio not available")
        except Exception as e:
            raise e

    async def user_social_bio_fetch(self, user_id: str = None) -> any:
        try:
            result = await self.collection.find_one({"_id": ObjectId(user_id)})

            if result:
                bio_dict = result.get("bio")
                users_followed_count = (
                    len(result.get("users_followed"))
                    if result.get("users_followed") is not None
                    else 0
                )
                users_following_count = (
                    result.get("users_following").get("total_followers")
                    if result.get("users_following")
                    else 0
                )

                self.collection(SOCIAL_POSTS)
                social_post_collection = SocialPostsCollection()
                like_count = await social_post_collection.post_likes_count_by_user_id(
                    user_id=user_id
                )

                social_profile_data = {
                    "id": str(result.get("_id")),
                    "name": result.get("full_name"),
                    "profile_image": result.get("profile_image")
                    if result.get("profile_image")
                    else None,
                    "current_city": result.get("current_city")
                    if result.get("current_city")
                    else None,
                    "about_me": bio_dict.get("about_me") if bio_dict else None,
                    "qualifications": bio_dict.get("qualifications")
                    if bio_dict
                    else None,
                    "experience": bio_dict.get("experience") if bio_dict else None,
                    "work_history": bio_dict.get("work_history") if bio_dict else None,
                    "current_company": bio_dict.get("current_company")
                    if bio_dict
                    else None,
                    "following": users_followed_count,
                    "followers": users_following_count,
                    "likes": like_count,
                }

                logging.info(social_profile_data)
                return social_profile_data

            raise HTTPException(status_code=200, detail="Bio not available")
        except Exception as e:
            raise e

    async def get_follower_count(self, user_id: ObjectId) -> int:
        try:
            result = await self.collection.find(
                finder={"_id": user_id},
                projection={"users_followed": 1, "_id": 0},
                return_doc_id=False,
            )
            return len(result[0]["users_followed"])
        except Exception as e:
            raise e

    async def update_profile_image_path(self, user_id, s3_path):
        try:
            find = {"_id": ObjectId(user_id)}
            user = await self.collection.find_one_and_modify(
                find,
                {"$set": {"profile_image": s3_path}},
                return_doc_id=False,
                return_updated_document=True,
            )

            return (
                {"is_profile_image_updated": True}
                if user
                else {"is_profile_image_updated": False}
            )
        except Exception as e:
            raise e

    async def update_create_user_profile_details(
        self, profile_details
    ) -> BaseIsUpdated:
        try:
            updater = {
                "$set": {
                    "full_name.first_name": profile_details.name,
                    "gender": profile_details.gender,
                    "current_city": profile_details.current_city,
                    "current_area": profile_details.current_area,
                    "bio.is_fresher": profile_details.is_fresher,
                    "bio.last_institute_name": profile_details.last_institute_name,
                    "bio.education": profile_details.education,
                    "bio.job_type": profile_details.job_type,
                    "bio.current_company": profile_details.recent_company_name,
                    "bio.experience_range": profile_details.experience_range,
                }
            }
            find = {"_id": ObjectId(profile_details.user_id)}
            user = await self.collection.find_one_and_modify(
                find,
                update=updater,
                return_doc_id=False,
                return_updated_document=True,
            )

            data = BaseIsUpdated(id=str(user.get("_id")), is_updated=True)
            return data
        except Exception as e:
            raise e
