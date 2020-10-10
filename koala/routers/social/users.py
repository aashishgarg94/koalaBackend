import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security
from koala.authentication.authentication_user import get_current_active_user
from koala.constants import REQUEST_LIMIT
from koala.crud.jobs_crud.user import MongoDBUserDatabase
from koala.crud.social.users import SocialPostsCollection
from koala.models.jobs_models.master import BaseIsCreated, BaseIsUpdated
from koala.models.jobs_models.user import UserInModel, UserModel
from koala.models.social.groups import GroupsFollowed, UsersFollowed
from koala.models.social.users import (
    BaseCommentsModel,
    BaseCreatePostModel,
    BaseFollowerModel,
    BaseIsFollowed,
    BaseLikeModel,
    BasePostMemberCountListModel,
    BasePostOwnerModel,
    BasePostReportModel,
    BaseShare,
    BaseShareModel,
    CommentInModel,
    CreatePostModelIn,
    CreatePostModelOut,
    CreatePostModelOutList,
    CreatePostModelPaginationModel,
    FollowerModel,
    ShareModel,
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
        raise e


@router.post(
    "/create_post",
    response_model=BaseIsCreated,
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def create_post(
    post_details: BaseCreatePostModel,
    is_group_post: bool,
    group_id: Optional[str] = None,
    current_user: UserModel = Depends(get_current_active_user),
):
    if is_group_post is True and group_id is None:
        raise HTTPException(
            status_code=400, detail="group_id is required with group post True"
        )
    try:
        social_posts_collection = SocialPostsCollection()

        user_map = get_user_model(current_user, "owner")
        post_details = CreatePostModelIn(**post_details.dict(), owner=user_map)

        shares = BaseShare(
            whatsapp=BaseShareModel(total_share=0, shared_by=[]),
            in_app_share=BaseShareModel(total_share=0, shared_by=[]),
        )

        likes = BaseLikeModel(total_likes=0, liked_by=[])

        post_report = BasePostReportModel(total_report=0, reported_by=[])

        return await social_posts_collection.create_post(
            post_details=post_details,
            is_group_post=is_group_post,
            group_id=group_id,
            shares=shares,
            likes=likes,
            post_report=post_report,
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/all_posts",
    response_model=CreatePostModelPaginationModel,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_all_posts(page_no: Optional[int] = 1):
    try:
        social_posts_collection = SocialPostsCollection()

        post_count = await social_posts_collection.get_count()

        user_list = []
        if post_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            user_list = await social_posts_collection.get_user_all_posts(
                skip=skip, limit=REQUEST_LIMIT
            )

        return CreatePostModelPaginationModel(
            total_posts=post_count, current_page=page_no, posts=user_list
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/post_by_post_id",
    response_model=CreatePostModelOut,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_post_by_post_id(post_id: str):
    try:
        social_posts_collection = SocialPostsCollection()
        return await social_posts_collection.get_user_post_by_post_id(post_id=post_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/post_by_user_id",
    response_model=CreatePostModelOutList,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_post_by_user_id(user_id: str):
    try:
        social_posts_collection = SocialPostsCollection()

        user_post_count = await social_posts_collection.get_user_post_count_by_user_id(
            user_id=user_id
        )
        if user_post_count > 0:
            return await social_posts_collection.get_user_post_by_user_id(
                user_id=user_id
            )
        else:
            return CreatePostModelOutList(post_list=[])
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/followed_groups",
    response_model=GroupsFollowed,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_followed_groups(user_id: str):
    try:
        social_posts_collection = SocialPostsCollection()
        return await social_posts_collection.get_user_followed_groups(user_id=user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/follow_user",
    response_model=BaseIsFollowed,
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def make_user_follow_group(
    user_id: str, current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_map = get_user_model(current_user, "follower")

        social_posts_collection = SocialPostsCollection()
        data = await social_posts_collection.make_user_follow_user(
            user_id=user_id, user_map=user_map
        )
        return data
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/user_followed",
    response_model=UsersFollowed,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_followed(
    page_no: Optional[int] = 1,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_id = get_user_model(current_user, "id")
        user_db = MongoDBUserDatabase(UserInModel)
        user_count = await user_db.get_follower_count(user_id)

        if user_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT

            social_posts_collection = SocialPostsCollection()
            return await social_posts_collection.get_user_followed(
                user_id=user_id, skip=skip, limit=REQUEST_LIMIT
            )
        else:
            return UsersFollowed(post_list=[])
    except Exception as e:
        logging.info(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/user_following",
    response_model=FollowerModel,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_following(
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_id = get_user_model(current_user, "id")
        social_posts_collection = SocialPostsCollection()
        return await social_posts_collection.get_user_following(user_id=user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/feed",
    response_model=CreatePostModelOutList,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_following(page_no: Optional[int] = 1):
    try:
        social_posts_collection = SocialPostsCollection()
        post_count = await social_posts_collection.get_feed_count()

        if post_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            return await social_posts_collection.get_user_feed(
                skip=skip, limit=REQUEST_LIMIT
            )
        else:
            return CreatePostModelOutList(post_list=[])
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/action/like",
    response_model=BaseIsUpdated,
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def get_user_following(
    post_id: str,
    like: bool = False,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        social_posts_collection = SocialPostsCollection()
        return await social_posts_collection.post_action(
            post_id=post_id, like=like, user_id=current_user.id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/action/share",
    response_model=BaseIsUpdated,
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def get_user_following(
    post_id: str,
    share: ShareModel = ShareModel.whatsapp,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        social_posts_collection = SocialPostsCollection()
        return await social_posts_collection.post_action(
            post_id=post_id, share=share, user_id=current_user.id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/action/comment",
    response_model=BaseIsUpdated,
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def get_user_following(
    post_id: str,
    comments: CommentInModel,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        social_posts_collection = SocialPostsCollection()
        comments = BaseCommentsModel(
            name=current_user.full_name, email=current_user.email, comments=comments
        )
        return await social_posts_collection.post_action(
            post_id=post_id, comments=comments, user_id=current_user.id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/action/report",
    response_model=BaseIsUpdated,
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def get_user_following(
    post_id: str,
    report_post: bool = False,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        social_posts_collection = SocialPostsCollection()
        return await social_posts_collection.post_action(
            post_id=post_id, report_post=report_post, user_id=current_user.id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


# Get social bio
@router.get(
    "/social/bio",
    dependencies=[Security(get_current_active_user, scopes=["applicant:read"])],
)
async def user_bio_fetch(user_id: str = None):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        return await user_db.user_social_bio_fetch(user_id=user_id)
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


@router.post(
    "/same_company_users",
    response_model=BasePostMemberCountListModel,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_following(
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        social_posts_collection = SocialPostsCollection()
        return await social_posts_collection.get_users_in_same_company(
            current_company=current_user.bio.current_company
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
