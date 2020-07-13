from koala.config.collections import GIG_TYPE, OP_AREAS, OP_CITIES
from koala.db.mongodb import db
from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.master import GigTypeModal, OpAreaModal, OpCityModal


class MasterCollections:
    gig_type_collection: AsyncIOMotorCollection

    def __init__(self):
        self.gig_type_collection = db.client["koala-backend"][GIG_TYPE]
        self.op_cities_collection = db.client["koala-backend"][OP_CITIES]
        self.op_area_collection = db.client["koala-backend"][OP_AREAS]

    async def get_all_gig_types(self):
        gigs_cursor = self.gig_type_collection.find()
        gigs_types = []
        for document in await gigs_cursor.to_list(length=100):
            gigs_types.append(document["name"])
        return GigTypeModal(**{"gig_types": gigs_types})

    async def get_op_cities(self):
        cities_cursor = self.op_cities_collection.find()
        cities = []
        for document in await cities_cursor.to_list(length=100):
            cities.append(document["name"])
        return OpCityModal(**{"op_cities": cities})

    async def get_op_areas(self):
        areas_cursor = self.op_area_collection.find()
        areas = []
        for document in await areas_cursor.to_list(length=100):
            areas.append(document["name"])
        return OpAreaModal(**{"op_areas": areas})
