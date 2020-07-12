from fastapi import APIRouter

from ..crud.master import MasterCollections
from ..models.master import GigTypeModal

router = APIRouter()


# Get all gigs
@router.get("/gigs/", response_model=GigTypeModal)
async def get_gig_type():
    master_collection = MasterCollections()
    return await master_collection.get_all_gig_types()
