import pprint
from typing import List

from ..db.mongodb import AsyncIOMotorClient
from ..models.user import UserInDB
from ..db.mongodb import db


async def get_comments_for_article(conn: AsyncIOMotorClient) -> List[UserInDB]:
    comments: List[UserInDB] = []
    rows = db.client['koala-backend']['test-users'].find()
    pprint.pprint(rows)
    async for row in rows:
        comments.append(UserInDB(**row))

    return comments
