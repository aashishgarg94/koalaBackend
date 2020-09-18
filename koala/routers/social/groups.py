import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from koala.authentication.authentication import get_current_active_user
from koala.constants import REQUEST_LIMIT
from koala.crud.social.groups import SocialGroupsCollection
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.jobs_models.user import UserModel
from koala.models.social.groups import (
    BasePostListModel,
    BaseSocialGroup,
    BaseSocialPostModel,
    GroupsWithPaginationModel,
    SocialGroupCreateIn,
    SocialGroupCreateOut,
)
from koala.models.social.users import BaseIsFollowed, FollowerModel
from koala.routers.social.users import get_user_model

router = APIRouter()


@router.post("/create", response_model=BaseIsCreated)
async def create_group(
    group_details: BaseSocialGroup,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_map = get_user_model(current_user, "owner")
        posts = BaseSocialPostModel()
        followers = FollowerModel()
        group_details = SocialGroupCreateIn(
            **group_details.dict(), posts=posts, owner=user_map, followers=followers
        )

        master_collection = SocialGroupsCollection()
        return await master_collection.create_group(group_details=group_details)
    except Exception as e:
        logging.info(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/get_all", response_model=GroupsWithPaginationModel)
async def get_all_groups(page_no: Optional[int] = 1):
    try:
        master_collection = SocialGroupsCollection()
        groups_count = await master_collection.get_count()

        group_list = []
        if groups_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            group_list = await master_collection.get_all_groups(skip, REQUEST_LIMIT)

        return GroupsWithPaginationModel(
            total_groups=groups_count, current_page=page_no, groups=group_list
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/group_by_id", response_model=SocialGroupCreateOut)
async def get_group_by_id(group_id: str):
    try:
        master_collection = SocialGroupsCollection()
        return await master_collection.get_group_by_id(group_id=group_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/follow_group", response_model=BaseIsFollowed)
async def make_user_follow_group(
    group_id: str, current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_map = get_user_model(current_user, "follower")

        master_collection = SocialGroupsCollection()
        return await master_collection.followGroup(group_id=group_id, user_map=user_map)
    except Exception as e:
        logging.info(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


# In progress
@router.post("/inprogress/create_post", response_model=dict)
async def get_group_users(group_id: str, user_id: str):
    try:
        master_collection = SocialGroupsCollection()
        data = await master_collection.get_group_users(group_id)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


# In progress
@router.post("/inprogress/all_users", response_model=dict)
async def get_group_users(group_id: str):
    try:
        master_collection = SocialGroupsCollection()
        data = await master_collection.get_group_users(group_id)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
