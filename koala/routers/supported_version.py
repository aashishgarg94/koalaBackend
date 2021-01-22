import logging

from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/supported_version",
)
async def supported_version(app_version: str, build_version: str):
    logging.info(app_version)
    logging.info(build_version)
    allowed_version = ['1.1.6', '1.1.7', '1.1.8', '1.1.9']
    if app_version in allowed_version:
        return False
    return True
