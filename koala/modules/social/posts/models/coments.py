from datetime import datetime
from typing import Optional, List

from pydantic import Field
from pydantic.main import BaseModel
from koala.core.mongo_model import OID


class BasePostCommentsModel(BaseModel):
    user_id: OID = Field()
    comment: str
    commented_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class BasePostCommentInModel(BaseModel):
    post_id: OID = Field()
    total_comments: Optional[int] = 0
    comments: Optional[List[BasePostCommentsModel]] = []
