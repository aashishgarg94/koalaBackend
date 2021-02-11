from typing import List, Optional

from koala.core.mongo_model import OID, MongoModel
from pydantic import BaseModel, Field

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

class CreateLearningCategoriesModelIn(BaseLearningCategoriesModel):
    is_deleted: Optional[bool] = False

class CreateLearningVideosModelIn(BaseLearningVideosModel):
    is_deleted: Optional[bool] = False

class CreateLearningCategoriesModelOut(BaseLearningCategoriesModel):
    id: OID = Field()

class CreateLearningCategoriesModelOutList(MongoModel):
    categories_list: List[CreateLearningCategoriesModelOut]

class CreateLearningVideosModelOut(BaseLearningVideosModel):
    id: OID = Field()

class CreateLearningVideosModelOutList(MongoModel):
    videos_list: List[CreateLearningVideosModelOut]