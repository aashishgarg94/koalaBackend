from fastapi import APIRouter, HTTPException
from koala.crud.jobs_crud.master import MasterCollections

router = APIRouter()


@router.get(
    "/generate_otp",
)
async def generate_otp(mobile_number: str):
    try:
        master_collection = MasterCollections()
        return await master_collection.generate_otp(mobile_number)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/verify_otp",
)
async def generate_otp(mobile_number: str, otp: str):
    try:
        master_collection = MasterCollections()
        return await master_collection.verify_otp(mobile_number, otp)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
