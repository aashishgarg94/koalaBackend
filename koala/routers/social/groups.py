import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Security, UploadFile
from koala.authentication.authentication_user import get_current_active_user
from koala.constants import REQUEST_LIMIT
from koala.crud.jobs_crud.user import MongoDBUserDatabase
from koala.crud.social.groups import SocialGroupsCollection
from koala.crud.social.users import SocialPostsCollection
from koala.models.jobs_models.master import BaseIsCreated, BaseIsDisabled
from koala.models.jobs_models.user import UserInModel, UserModel
from koala.models.social.groups import (
    BaseGroupMemberCountListModel,
    BaseSocialPostModel,
    GroupsWithPaginationModel,
    SocialGroupCreateIn,
    SocialGroupCreateOut,
)
from koala.models.social.users import (
    BaseFollowerModel,
    BaseIsFollowed,
    CreatePostModelOutList,
    FollowerModel,
)
from koala.routers.social.users import get_user_model

router = APIRouter()


@router.post(
    "/create",
    response_model=BaseIsCreated,
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def create_group(
    # group_details: BaseSocialGroup,
    file: UploadFile = File(None),
    group_name: str = Form(...),
    group_industry_type: str = Form(...),
    group_description: str = Form(...),
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_map = get_user_model(current_user, "owner")
        posts = BaseSocialPostModel()
        followers = FollowerModel(
            total_followers=1,
            followers_list=[
                BaseFollowerModel(
                    name=current_user.full_name,
                    username=current_user.username,
                    user_id=current_user.id,
                    followed_on=datetime.now(),
                )
            ],
        )
        group_details = SocialGroupCreateIn(
            groupName=group_name,
            groupDescription=group_description,
            posts=posts,
            owner=user_map,
            followers=followers,
        )

        social_groups_collection = SocialGroupsCollection()
        return await social_groups_collection.create_group(
            group_details=group_details, file=file, user_id=current_user.id
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/get_all",
    response_model=GroupsWithPaginationModel,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_all_groups(
    page_no: Optional[int] = 1,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        user_current_group_list = await user_db.find_groups_followed_by_username(
            username=current_user.username
        )

        group_list = []
        # if len(user_current_group_list[0].get("groups_followed")) > 0:
        adjusted_page_number = page_no - 1
        skip = adjusted_page_number * REQUEST_LIMIT
        social_groups_collection = SocialGroupsCollection()
        group_list = await social_groups_collection.get_all_groups(
            skip,
            REQUEST_LIMIT,
            current_groups=user_current_group_list[0].get("groups_followed"),
        )

        return GroupsWithPaginationModel(
            total_groups=len(user_current_group_list[0].get("groups_followed")),
            current_page=page_no,
            groups=group_list,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/group_by_id",
    response_model=SocialGroupCreateOut,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_group_by_id(group_id: str):
    try:
        social_groups_collection = SocialGroupsCollection()
        return await social_groups_collection.get_group_by_id(group_id=group_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/follow_group",
    response_model=BaseIsFollowed,
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def make_user_follow_group(
    group_id: str,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_map = get_user_model(current_user, "follower")

        social_groups_collection = SocialGroupsCollection()
        return await social_groups_collection.followGroup(
            group_id=group_id, user_map=user_map
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/all_users",
    response_model=FollowerModel,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_group_users(group_id: str):
    try:
        social_groups_collection = SocialGroupsCollection()
        return await social_groups_collection.get_group_users(group_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/posts",
    response_model=CreatePostModelOutList,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_group_posts(group_id: str, page_no: Optional[int] = 1):
    try:
        social_posts_collection = SocialPostsCollection()
        post_count = await social_posts_collection.get_feed_count(is_group_post=True)

        if post_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            return await social_posts_collection.get_group_posts(
                group_id=group_id, skip=skip, limit=REQUEST_LIMIT
            )
        else:
            return CreatePostModelOutList(post_list=[])
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/groups_by_user_id",
    response_model=BaseGroupMemberCountListModel,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def groups_by_user_id(
    user_id: str = None,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        social_groups_collection = SocialGroupsCollection()

        search_user_id = user_id
        if user_id is None:
            search_user_id = current_user.id
        user_groups = await social_groups_collection.get_groups_by_user_id(
            user_id=search_user_id
        )

        if len(user_groups) > 0:
            return await social_groups_collection.get_group_details(
                groups_list=user_groups[0].get("groups_followed")
            )

        return BaseGroupMemberCountListModel(user_groups=[])
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/disable_group_by_group_id",
    response_model=BaseIsDisabled,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def disable_group_by_group_id(
    group_id: str,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        social_groups_collection = SocialGroupsCollection()
        disabled_group = await social_groups_collection.disable_group_by_group_id(group_id=group_id)

        social_posts_collection = SocialPostsCollection()
        result = await social_posts_collection.disable_multiple_post_by_post_ids(
            post_ids=disabled_group.get('posts').get('post_list')
        )
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/group_users",
    response_model=None,
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def group_delete_user_by_id(
    group_id: str,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        social_groups_collection = SocialGroupsCollection()
        response = await social_groups_collection.get_group_users_details(group_id=group_id)
        return response
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
