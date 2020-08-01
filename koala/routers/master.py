from fastapi import APIRouter, HTTPException

from ..crud.master import MasterCollections
from ..models.jobs import JobInfo
from ..models.master import GigTypeModel, OpAreaModel, OpCityModel

router = APIRouter()


# Get all gigs
@router.get("/gigs/", response_model=GigTypeModel)
async def get_gig_type():
    master_collection = MasterCollections()
    return await master_collection.get_all_gig_types()


# TODO: For now getting the cities we operate in later we can get them by states
# Get cities we operate in
@router.get("/op_cities/", response_model=OpCityModel)
async def get_op_cities():
    master_collection = MasterCollections()
    return await master_collection.get_op_cities()


@router.get("/op_area/", response_model=OpAreaModel)
async def get_op_cities():
    master_collection = MasterCollections()
    return await master_collection.get_op_areas()


@router.get("/job/job_info", response_model=JobInfo)
async def get_job_info():
    master_collection = MasterCollections()
    try:
        return await master_collection.get_job_info()
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
