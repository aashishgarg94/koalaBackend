import logging
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Security, UploadFile
from fastapi.params import File
from koala.authentication.authentication_user import get_current_active_user
from koala.aws.constants import POST_CREATE
from koala.aws.producers.posts import post_producer
from koala.models.jobs_models.user import UserModel
from koala.modules.social.posts.crud.posts import Posts
from koala.modules.social.posts.models.posts import (
    BasePostModel,
    BaseMediaTypeModel,
    BasePostUpdateModel,
)

router = APIRouter()


@router.post(
    "/create_post",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def create_post(
    media_type: BaseMediaTypeModel,
    is_group_post: bool,
    group_id: Optional[str] = None,
    file: UploadFile = File(None),
    content: str = Form(None),
    tags: list = Form(None),
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        post_details = BasePostModel(
            media_type=media_type,
            content=content,
            tags=tags if tags else [],
            owner=current_user.id,
            is_group_post=is_group_post,
            group_id=group_id if is_group_post else None,
        )

        posts = Posts()
        post_id = await posts.create_post(post_details=post_details, file=file)

        if post_id:
            # Publish event to topic
            post_producer(
                event=POST_CREATE,
                detail={"post_id": str(post_id), "owner_id": str(current_user.id)},
            )
            # Return response to user
            return {"status_code": 200, "post_id": str(post_id)}
        else:
            return {"status_code": 503, "error": {"msg": "Not able to create post"}}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/update_post",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def update_post(
    post_id: str,
    media_type: BaseMediaTypeModel,
    file_url: Optional[str] = None,
    file: UploadFile = File(None),
    content: str = Form(None),
    tags: list = Form(None),
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        post_details = BasePostUpdateModel(
            media_type=media_type,
            media_url=file_url,
            content=content,
            tags=tags if tags else [],
            owner=current_user.id,
        )

        posts = Posts()
        post_id = await posts.update_post(
            post_id=post_id, post_details=post_details, file=file
        )
        if post_id:
            return {"status_code": 200, "post_id": str(post_id.get("_id"))}
        elif post_id is None:
            return {"status_code": 404, "error": {"msg": "Post Not Found"}}
        else:
            return {"status_code": 503, "error": {"msg": "Not able to update post"}}

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/disable_by_post_id",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def disable_by_post_id(
    post_id: str,
):
    try:
        posts = Posts()
        post_id = await posts.disable_by_post_id(post_id=post_id)
        if post_id:
            return {"status_code": 200, "post_id": str(post_id.get("_id"))}
        elif post_id is None:
            return {"status_code": 404, "error": {"msg": "Post Not Found"}}
        else:
            return {"status_code": 503, "error": {"msg": "Not able to delete post"}}
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/report_post",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def report_post(
    post_id: str,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        posts = Posts()
        post_id = await posts.report_post(post_id=post_id)
        if post_id:
            # TODO: Push post_id and user_id (user_id=current_user.id) in Queue with event_type = POST_REPORTED and
            #  remove it from all users in consumers
            return {"status_code": 200, "post_id": str(post_id.get("_id"))}
        elif post_id is None:
            return {"status_code": 404, "error": {"msg": "Post Not Found"}}
        else:
            return {"status_code": 503, "error": {"msg": "Not able to report post"}}
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/all_posts",
#     response_model=CreatePostModelPaginationModel,
#     dependencies=[Security(get_current_active_user, scopes=["social:read"])],
# )
# async def get_user_all_posts(page_no: Optional[int] = 1):
#     try:
#         social_posts_collection = SocialPostsCollection()
#
#         post_count = await social_posts_collection.get_count()
#
#         more_pages = True
#         post_list = []
#         if post_count > 0:
#             adjusted_page_number = page_no - 1
#             skip = adjusted_page_number * REQUEST_LIMIT
#             post_list = await social_posts_collection.get_user_all_posts(
#                 skip=skip, limit=REQUEST_LIMIT
#             )
#
#             if page_no == math.ceil(post_count / REQUEST_LIMIT):
#                 more_pages = False
#
#             # TODO: Shuffling is temp, once the planned db changes done, must remove this
#             # random.shuffle(post_list)
#
#         return CreatePostModelPaginationModel(
#             more_pages=more_pages, post_list=post_list
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")
#
#
# @router.post(
#     "/post_by_post_id",
#     response_model=CreatePostModelOut,
#     dependencies=[Security(get_current_active_user, scopes=["social:read"])],
# )
# async def get_user_post_by_post_id(post_id: str):
#     try:
#         social_posts_collection = SocialPostsCollection()
#         return await social_posts_collection.get_user_post_by_post_id(post_id=post_id)
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")
#
#
# @router.post(
#     "/post_by_user_id",
#     response_model=CreatePostModelOutList,
#     dependencies=[Security(get_current_active_user, scopes=["social:read"])],
# )
# async def get_user_post_by_user_id(user_id: str):
#     try:
#         social_posts_collection = SocialPostsCollection()
#
#         user_post_count = await social_posts_collection.get_user_post_count_by_user_id(
#             user_id=user_id
#         )
#         if user_post_count > 0:
#             return await social_posts_collection.get_user_post_by_user_id(
#                 user_id=user_id
#             )
#         else:
#             return CreatePostModelOutList(post_list=[])
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")
#
#

# @router.post(
#     "/post_by_tags",
#     response_model=CreatePostModelOutList,
#     dependencies=[Security(get_current_active_user, scopes=["social:read"])],
# )
# async def get_user_followed(posts_tags: PostByTagInModel, page_no: Optional[int] = 1):
#     try:
#         adjusted_page_number = page_no - 1
#         skip = adjusted_page_number * REQUEST_LIMIT
#
#         social_posts_collection = SocialPostsCollection()
#         return await social_posts_collection.get_posts_by_tags(
#             tags=posts_tags.tags, skip=skip, limit=REQUEST_LIMIT
#         )
#     except Exception as e:
#         logging.info(e)
#         raise HTTPException(status_code=500, detail="Something went wrong")
#
#
