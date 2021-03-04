from fastapi import HTTPException
from koala.models.jobs_models.master import BaseIsCreated
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.config.collections import COINS
from koala.crud.jobs_crud.user import MongoDBUserDatabase
from koala.models.social.users import CreateCoinsModelIn
from koala.models.jobs_models.user import UserInModel


class CoinsCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(COINS)

    async def coins_added(
        self, coins_details: CreateCoinsModelIn, user_id: str, coins: int
    ) -> any:
        try:
            insert_id = await self.collection.insert_one(
                coins_details.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )

            users_collection = MongoDBUserDatabase(UserInModel)
            await users_collection.user_increment_coins(user_id=user_id, coins=coins)

            return BaseIsCreated(id=insert_id, is_created=True) if insert_id else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
