import logging
from typing import Optional, List
from bson import ObjectId
from fastapi import APIRouter, Depends, Form, HTTPException, Security
from koala.authentication.authentication_user import get_current_active_user
from koala.crud.learning.learning_categories import LearningCategoriesCollection
from koala.crud.learning.learning_videos import LearningVideosCollection
from koala.crud.learning.videos_watched import VideosWatchedCollection
from koala.crud.social.streaks import StreaksCollection
from koala.models.jobs_models.user import UserModel
from koala.models.learning.learning import (
    BaseLearningCategoriesModel,
    BaseLearningVideosModel,
    CreateLearningCategoriesModelIn,
    CreateLearningVideosModelIn,
    CreateVideoWatchedModelIn,
    CreateLearningCategoriesModelOut,
    CreateLearningCategoriesModelOutList,
    CreateLearningVideosModelOut,
    CreateLearningVideosModelOutList
)

router = APIRouter()

@router.post(
    "/create_learning_category",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def create_learning_category(
    title: str = Form(None),
    image: Optional[str] = None
):
    try:
        learning_categories_collection = LearningCategoriesCollection()

        category_details = CreateLearningCategoriesModelIn(
            title=title,
            image=image,
            is_deleted=False
        )

        return await learning_categories_collection.create_learning_category(
            category_details=category_details
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/update_learning_category",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def update_learning_category(
    category_id: str = Form(None),
    title: str = Form(None),
    image: Optional[str] = None
):
    try:
        learning_categories_collection = LearningCategoriesCollection()

        response = await learning_categories_collection.update_learning_category(
            category_id=category_id,
            title=title,
            image=image
        )
        return response
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/all_learning_categories",
    response_model=CreateLearningCategoriesModelOutList,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_all_learning_categories(page_no: Optional[int] = 1):
    try:
        learning_categories_collection = LearningCategoriesCollection()

        categories_list = []
        categories_list = await learning_categories_collection.get_all_learning_categories()
        #return post_list

        return CreateLearningCategoriesModelOutList(
            categories_list=categories_list
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/create_learning_video",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def create_learning_video(
    title: str = None,
    category: str = None,
    category_id: str = None,
    lesson_number: int = None,
    video_id: str = None,
    description: Optional[str] = None,
    image: Optional[str] = None
):
    try:
        learning_videos_collection = LearningVideosCollection()

        video_details = CreateLearningVideosModelIn(
            title=title,
            category=category,
            category_id=category_id,
            lesson_number=lesson_number,
            video_id=video_id,
            description=description,
            image=image,
            is_deleted=False
        )

        return await learning_videos_collection.create_learning_video(
            video_details=video_details
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/create_learning_videos_list",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def create_learning_videos_list(
    videos_list: List[CreateLearningVideosModelIn],
):
    try:
        learning_videos_collection = LearningVideosCollection()

        if videos_list is not None:
            for video in videos_list:
                video_details = CreateLearningVideosModelIn(
                    title=video.title,
                    category=video.category,
                    category_id=video.category_id,
                    lesson_number=video.lesson_number,
                    video_id=video.video_id,
                    description=video.description,
                    image=video.image,
                    is_deleted=False
                )

                await learning_videos_collection.create_learning_video(
                    video_details=video_details
                )
                
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/update_learning_video",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def update_learning_video(
    element_id: str = None,
    video_id: str = None,
    title: str = None,
    category: str = None,
    category_id: str = None,
    lesson_number: int = None,
    description: Optional[str] = None,
    image: Optional[str] = None
):
    try:
        learning_videos_collection = LearningVideosCollection()

        response = await learning_videos_collection.update_learning_video(
            element_id=element_id,
            video_id=video_id,
            title=title,
            category=category,
            category_id=category_id,
            lesson_number=lesson_number,
            description=description,
            image=image
        )
        return response
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/all_learning_videos",
    response_model=CreateLearningVideosModelOutList,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_all_learning_videos(
        category_id: str,
    ):
    try:
        learning_videos_collection = LearningVideosCollection()

        videos_list = []
        videos_list = await learning_videos_collection.get_all_learning_videos(category_id=category_id)

        return CreateLearningVideosModelOutList(
            videos_list=videos_list
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/video_started",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def video_started(
    video_id: str,
    current_user: UserModel = Depends(get_current_active_user)
):
    try:
        learning_videos_collection = LearningVideosCollection()

        await learning_videos_collection.video_watched_action(
            video_id=video_id, started=True, user_id=current_user.id
        )

        streaks_collection = StreaksCollection()

        await streaks_collection.video_streak(
            video_id=video_id, started=True, user_id=current_user.id
        )

        videos_watched_collection = VideosWatchedCollection()

        video_watched_details = CreateVideoWatchedModelIn(
            video_id=video_id,
            user_id=ObjectId(current_user.id),
            is_started_log=True,
            is_finished_log=False
        )

        return await videos_watched_collection.video_watched_action(
            video_watched_details=video_watched_details
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/video_finished",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def video_finished(
    video_id: str,
    current_user: UserModel = Depends(get_current_active_user)
):
    try:
        learning_videos_collection = LearningVideosCollection()

        await learning_videos_collection.video_watched_action(
            video_id=video_id, finished=True, user_id=current_user.id
        )

        videos_watched_collection = VideosWatchedCollection()

        video_watched_details = CreateVideoWatchedModelIn(
            video_id=video_id,
            user_id=ObjectId(current_user.id),
            is_started_log=False,
            is_finished_log=True
        )

        return await videos_watched_collection.video_watched_action(
            video_watched_details=video_watched_details
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


