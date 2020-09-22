from fastapi import APIRouter, HTTPException, Security
from koala.crud.jobs_crud.master import MasterCollections
from koala.models.jobs_models.master import (
    GigTypeModel,
    JobMasterModel,
    OpAreaModel,
    OpCityModel,
)

router = APIRouter()


# Get all gigs
@router.get(
    "/gigs",
    response_model=GigTypeModel,
    dependencies=[Security(scopes=["applicant:read", "master:write"])],
)
async def get_gig_type():
    try:
        master_collection = MasterCollections()
        return await master_collection.get_all_gig_types()
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


# TODO: For now getting the cities we operate in later we can get them by states
# Get cities we operate in
@router.get(
    "/op_cities",
    response_model=OpCityModel,
    dependencies=[Security(scopes=["applicant:read", "master:write"])],
)
async def get_op_cities():
    try:
        master_collection = MasterCollections()
        return await master_collection.get_op_cities()
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/op_area",
    response_model=OpAreaModel,
    dependencies=[Security(scopes=["applicant:read", "master:write"])],
)
async def get_op_cities():
    try:
        master_collection = MasterCollections()
        return await master_collection.get_op_areas()
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/job/job_master",
    response_model=JobMasterModel,
    dependencies=[Security(scopes=["applicant:read", "master:write"])],
)
async def get_job_master():
    try:
        master_collection = MasterCollections()
        result = await master_collection.get_job_master()
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
