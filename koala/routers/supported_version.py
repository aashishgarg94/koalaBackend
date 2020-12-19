from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get(
    "/supported_version",
)
async def generate_otp():
    return ['1.0.0', '1.2.0']
