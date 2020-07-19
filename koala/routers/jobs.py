import logging
from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException

from ..constants import REQUEST_LIMIT, REQUEST_SKIP
from ..crud.jobs import JobsCollection
from ..models.jobs import BaseJobModel, BaseJobModelDB, JobCreatedOut

router = APIRouter()

DUMMY_COMPANY_ID = "100-workforce"


@router.post("/jobs/create/", response_model=JobCreatedOut)
async def job_create(job_info: BaseJobModel):
    job_info_to_db = BaseJobModelDB(
        **job_info.dict(exclude_unset=True),
        posted_on=date.today(),
        company_id=DUMMY_COMPANY_ID
    )
    jobs_collection = JobsCollection()
    try:
        job_create_response = await jobs_collection.job_create(job_info_to_db)
        if job_create_response is False:
            raise HTTPException(status_code=400, detail="Not able to process")
        return JobCreatedOut(job_id=job_create_response, is_created=True)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


# USER skip AND limit for querying data. Will be used for pagination
@router.get("/jobs/getAll/")
async def job_get_all(
    skip: Optional[int] = REQUEST_SKIP, limit: Optional[int] = REQUEST_LIMIT
):
    # Only send the information required to display on cards
    pass


# TODO: Get encoded job_id - Decide on encoder
@router.get("/jobs/get/{job_id}/")
async def get_job_by_id(job_id: int):
    # Get all the information as this is the details page for a particular job
    pass


@router.post("/jobs/update/")
async def job_update():
    # Anything can be update regarding a job from here
    pass


@router.post("/jobs/delete/")
async def job_delete_by_id():
    # Delete multiple from frontend using multiple checkbox or delete one - Same process
    pass
