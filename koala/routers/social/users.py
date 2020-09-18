import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from koala.authentication.authentication import get_current_active_user
from koala.constants import REQUEST_LIMIT
from koala.crud.social.users import SocialUsersCollection
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.jobs_models.user import UserModel
from koala.models.social.groups import GroupsFollowed
from koala.models.social.users import (
    BaseCreatePostModel,
    BaseFollowerModel,
    BaseIsFollowed,
    BasePostOwnerModel,
    CreatePostModelIn,
    CreatePostModelOut,
    CreatePostModelPaginationModel,
    FollowerModel,
    UserFollowed,
    UsersFollowing,
)

router = APIRouter()


def get_user_model(current_user: UserModel, get_type: str):
    try:
        # Get user
        user_name = current_user.full_name
        user_email = current_user.email
        user_id = current_user.id

        if get_type == "id":
            return user_id
        elif get_type == "owner":
            # Update owner
            return BasePostOwnerModel(name=user_name, email=user_email, user_id=user_id)
        elif get_type == "follower":
            # Update follower
            data = BaseFollowerModel(name=user_name, email=user_email, user_id=user_id)
            return data
    except Exception as e:
        logging.error(e)
        raise e


@router.post("/create_post", response_model=BaseIsCreated)
async def create_post(
    post_details: BaseCreatePostModel,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        master_collection = SocialUsersCollection()

        user_map = get_user_model(current_user, "owner")
        post_details = CreatePostModelIn(**post_details.dict(), owner=user_map)

        return await master_collection.create_post(post_details=post_details)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/all_posts", response_model=CreatePostModelPaginationModel)
async def get_user_all_posts(page_no: Optional[int] = 1):
    try:
        master_collection = SocialUsersCollection()

        user_count = await master_collection.get_count()

        user_list = []
        if user_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            user_list = await master_collection.get_user_all_posts(
                skip=skip, limit=REQUEST_LIMIT
            )

        return CreatePostModelPaginationModel(
            total_posts=user_count, current_page=page_no, posts=user_list
        )
    except Exception as e:
        logging.info(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/post_by_id", response_model=CreatePostModelOut)
async def get_user_post_by_id(post_id: str):
    try:
        master_collection = SocialUsersCollection()
        return await master_collection.get_user_post_by_id(post_id=post_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/followed_groups", response_model=GroupsFollowed)
async def get_user_followed_groups(user_id: str):
    try:
        logging.info(user_id)
        master_collection = SocialUsersCollection()
        return await master_collection.get_user_followed_groups(user_id=user_id)
    except Exception as e:
        logging.info(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/follow_user", response_model=BaseIsFollowed)
async def make_user_follow_group(
    user_id: str, current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_map = get_user_model(current_user, "follower")

        master_collection = SocialUsersCollection()
        data = await master_collection.make_user_follow_user(
            user_id=user_id, user_map=user_map
        )
        return data
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/user_followed", response_model=UserFollowed)
async def get_user_followed(current_user: UserModel = Depends(get_current_active_user)):
    try:
        user_id = get_user_model(current_user, "id")
        master_collection = SocialUsersCollection()
        return await master_collection.get_user_followed(user_id=user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/user_following", response_model=FollowerModel)
async def get_user_following(
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_id = get_user_model(current_user, "id")
        master_collection = SocialUsersCollection()
        return await master_collection.get_user_following(user_id=user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
