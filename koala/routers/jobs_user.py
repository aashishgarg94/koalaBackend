import pprint
from typing import Optional

from fastapi import APIRouter, Depends
# from koala.models.jobs import Base
from koala.authentication.authentication import get_current_active_user
from koala.models.user import UserModel

router = APIRouter()


# Apply for job
@router.post("/job/apply/")
async def job_apply(
    job_id: int, current_user: UserModel = Depends(get_current_active_user)
):
    pprint.pprint(current_user)


# Get all applied jobs, get user from token
@router.get("/user/jobs/")
async def user_get_all_jobs(page_no: Optional[int] = 1):
    pass


@router.get("/job/user/")
async def job_get_all_users(page_no: Optional[int] = 1):
    pass
