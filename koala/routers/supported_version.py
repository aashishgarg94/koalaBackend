from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get(
    "/supported_version",
)
async def generate_otp():
    try:
        return True;
    except Exception:
        raise HTTPException(status_code=500, detail="Can't pull supported versions")
