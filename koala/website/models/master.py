from koala.core.mongo_model import OID, MongoModel
from pydantic import Field


class BaseIsCreated(MongoModel):
    id: OID = Field()
    is_created: bool
