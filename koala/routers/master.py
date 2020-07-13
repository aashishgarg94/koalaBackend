from fastapi import APIRouter

from ..crud.master import MasterCollections
from ..models.master import GigTypeModal, OpAreaModal, OpCityModal

router = APIRouter()


# Get all gigs
@router.get("/gigs/", response_model=GigTypeModal)
async def get_gig_type():
    master_collection = MasterCollections()
    return await master_collection.get_all_gig_types()


# TODO: For now getting the cities we operate in later we can get them by states
# Get cities we operate in
@router.get("/op_cities/", response_model=OpCityModal)
async def get_op_cities():
    master_collection = MasterCollections()
    return await master_collection.get_op_cities()


@router.get("/op_area/", response_model=OpAreaModal)
async def get_op_cities():
    master_collection = MasterCollections()
    return await master_collection.get_op_areas()
