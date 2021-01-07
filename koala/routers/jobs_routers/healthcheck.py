from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class BaseHealthCheck(BaseModel):
    message: str
    status: int


@router.get("/healthcheck")
def healthcheck():
    msg = "I am good"
    return BaseHealthCheck(message=msg, status=200)
