from koala.config.collections import GIG_TYPE
from koala.db.mongodb import db
from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.master import GigTypeModal


class MasterCollections:
    gig_type_collection: AsyncIOMotorCollection

    def __init__(self):
        self.gig_type_collection = db.client["koala-backend"][GIG_TYPE]

    async def get_all_gig_types(self):

        gigs_cursor = self.gig_type_collection.find()
        gigs_types = []
        for document in await gigs_cursor.to_list(length=100):
            gigs_types.append(document["name"])
        return GigTypeModal(**{"names": gigs_types})
