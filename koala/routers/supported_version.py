import logging

from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/supported_version",
)
async def supported_version(app_version: str, build_version: str):
    logging.info(app_version)
    logging.info(build_version)
    allowed_version = ["1.1.11", "1.1.12", "1.1.14", "1.1.15"]
    if app_version in allowed_version:
        return False
    return True
