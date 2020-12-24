import logging

from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/supported_version",
)
async def supported_version(app_version: str, build_version: str):
    logging.info(app_version)
    logging.info(build_version)
    data = ['1.0.0', '1.2.0']
    return False
