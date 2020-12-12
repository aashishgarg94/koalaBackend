import logging

from fastapi import APIRouter, HTTPException
from koala.crud.jobs_crud.company import CompanyCollection
from pydantic import EmailStr, BaseModel

router = APIRouter()


class BaseHealthCheck(BaseModel):
    message: str
    status: int


@router.get("/healthcheck")
def healthcheck():
    msg = (
        "I am good"
    )
    return BaseHealthCheck(message=msg, status=200)