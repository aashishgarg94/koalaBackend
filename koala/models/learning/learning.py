from typing import List, Optional

from koala.core.mongo_model import OID, MongoModel
from pydantic import Field


class BaseLearningCategoriesModel(MongoModel):
    title: str = ""
    image: Optional[str] = None


class BaseLearningVideosModel(MongoModel):
    title: str = ""
    category: str = ""
    category_id: str = ""
    lesson_number: int = 0
    video_id: str = ""
    description: Optional[str] = None
    image: Optional[str] = None
    views_started: Optional[int] = None
    views_finished: Optional[int] = None
    views: Optional[str] = None


class BaseVideoWatchedModel(MongoModel):
    video_id: str = ""
    user_id: OID = Field()
    is_started_log: Optional[bool] = None
    is_finished_log: Optional[bool] = None


class CreateLearningCategoriesModelIn(BaseLearningCategoriesModel):
    is_deleted: Optional[bool] = False


class CreateLearningVideosModelIn(BaseLearningVideosModel):
    is_deleted: Optional[bool] = False


class CreateVideoWatchedModelIn(BaseVideoWatchedModel):
    is_deleted: Optional[bool] = False


class CreateLearningCategoriesModelOut(BaseLearningCategoriesModel):
    id: OID = Field()


class CreateLearningCategoriesModelOutList(MongoModel):
    categories_list: List[CreateLearningCategoriesModelOut]


class CreateLearningVideosModelOut(BaseLearningVideosModel):
    id: OID = Field()


class CreateLearningVideosModelOutList(MongoModel):
    videos_list: List[CreateLearningVideosModelOut]


class CreateVideoWatchedModelOut(MongoModel):
    id: OID = Field()
