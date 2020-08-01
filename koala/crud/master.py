from koala.config.collections import GIG_TYPE, JOB_MASTER, OP_AREAS, OP_CITIES
from koala.db.mongodb import db
from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.jobs import JobInfo
from ..models.master import GigTypeModel, OpAreaModel, OpCityModel


class MasterCollections:
    gig_type_collection: AsyncIOMotorCollection

    def __init__(self):
        self.gig_type_collection = db.client["koala-backend"][GIG_TYPE]
        self.op_cities_collection = db.client["koala-backend"][OP_CITIES]
        self.op_area_collection = db.client["koala-backend"][OP_AREAS]
        self.job_master_collection = db.client["koala-backend"][JOB_MASTER]

    async def get_all_gig_types(self) -> GigTypeModel:
        gigs_cursor = self.gig_type_collection.find()
        gigs_types = []
        for document in await gigs_cursor.to_list(length=100):
            gigs_types.append(document["name"])
        return GigTypeModel(**{"gig_types": gigs_types})

    async def get_op_cities(self) -> OpCityModel:
        cities_cursor = self.op_cities_collection.find()
        cities = []
        for document in await cities_cursor.to_list(length=100):
            cities.append(document["name"])
        return OpCityModel(**{"op_cities": cities})

    async def get_op_areas(self) -> OpAreaModel:
        areas_cursor = self.op_area_collection.find()
        areas = []
        for document in await areas_cursor.to_list(length=100):
            areas.append(document["name"])
        return OpAreaModel(**{"op_areas": areas})

    async def get_job_info(self) -> JobInfo:
        try:
            job_info_cursor = self.job_master_collection.find({}, {"_id": 0})
            job_info = {}
            for document in await job_info_cursor.to_list(length=100):
                job_info.update(document)
            return JobInfo(**{"job_info": job_info})
        except Exception as e:
            raise e
