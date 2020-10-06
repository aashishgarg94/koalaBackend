from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from koala.authentication.authentication_user import get_current_active_user
from koala.constants import REQUEST_LIMIT
from koala.crud.social.groups import SocialGroupsCollection
from koala.crud.social.users import SocialPostsCollection
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.jobs_models.user import UserModel
from koala.models.social.groups import (
    BaseSocialGroup,
    BaseSocialPostModel,
    GroupsWithPaginationModel,
    SocialGroupCreateIn,
    SocialGroupCreateOut,
)
from koala.models.social.users import (
    BaseIsFollowed,
    CreatePostModelOutList,
    FollowerModel,
)
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

        social_groups_collection = SocialGroupsCollection()
        return await social_groups_collection.create_group(group_details=group_details)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/get_all", response_model=GroupsWithPaginationModel)
async def get_all_groups(page_no: Optional[int] = 1):
    try:
        social_groups_collection = SocialGroupsCollection()
        groups_count = await social_groups_collection.get_count()

        group_list = []
        if groups_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            group_list = await social_groups_collection.get_all_groups(
                skip, REQUEST_LIMIT
            )

        return GroupsWithPaginationModel(
            total_groups=groups_count, current_page=page_no, groups=group_list
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/group_by_id", response_model=SocialGroupCreateOut)
async def get_group_by_id(group_id: str):
    try:
        social_groups_collection = SocialGroupsCollection()
        return await social_groups_collection.get_group_by_id(group_id=group_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/follow_group", response_model=BaseIsFollowed)
async def make_user_follow_group(
    group_id: str, current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_map = get_user_model(current_user, "follower")

        social_groups_collection = SocialGroupsCollection()
        return await social_groups_collection.followGroup(
            group_id=group_id, user_map=user_map
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/all_users", response_model=FollowerModel)
async def get_group_users(group_id: str):
    try:
        social_groups_collection = SocialGroupsCollection()
        return await social_groups_collection.get_group_users(group_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/posts", response_model=CreatePostModelOutList)
async def get_user_following(group_id: str, page_no: Optional[int] = 1):
    try:
        social_posts_collection = SocialPostsCollection()
        post_count = await social_posts_collection.get_feed_count(is_group_post=True)

        if post_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            return await social_posts_collection.get_user_feed(
                group_id=group_id, skip=skip, limit=REQUEST_LIMIT
            )
        else:
            return CreatePostModelOutList(post_list=[])
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
