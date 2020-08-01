from typing import Optional

from fastapi import APIRouter, HTTPException

from ..constants import REQUEST_LIMIT
from ..crud.jobs import JobsCollection
from ..models.jobs import BaseJobModel, JobInModel, JobOutModel, JobOutWithPagination
from ..models.master import BaseIsCreated, BaseIsDeleted, BaseIsUpdated

router = APIRouter()

DUMMY_COMPANY_ID = "100-workforce"


@router.post("/jobs/create/", response_model=BaseIsCreated)
async def job_create(job_info: BaseJobModel):
    job_detail = JobInModel(**job_info.dict())
    jobs_collection = JobsCollection()
    try:
        result = await jobs_collection.job_create(job_detail)
        if result is False:
            raise HTTPException(status_code=400, detail="Not able to process")
        return BaseIsCreated(job_id=result, is_created=True)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


# USER skip AND limit for querying data. Will be used for pagination
@router.get("/jobs/getAll/", response_model=JobOutWithPagination)
async def job_get_all(page_no: Optional[int] = 1):
    job_collection = JobsCollection()
    try:
        jobs_count = await job_collection.get_count()

        job_list = []
        if jobs_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            job_list = await job_collection.get_all(skip, REQUEST_LIMIT)

        return JobOutWithPagination(
            **{"total_jobs": jobs_count, "current_page": page_no, "jobs": job_list}
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


# TODO: Get encoded job_id - Decide on encoder
@router.get("/jobs/get/{job_id}/", response_model=JobOutModel)
async def get_job_by_id(job_id: int):
    job_collection = JobsCollection()
    try:
        job = await job_collection.get_by_id(job_id)
        return job if job else None
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/jobs/update/{job_id}", response_model=BaseIsUpdated)
async def job_update(job_id: int, job_detail: BaseJobModel):
    # Anything can be update regarding a job from here
    job_collection = JobsCollection()
    try:
        job_changes = JobInModel(**job_detail.dict())
        updated_job = await job_collection.find_and_update(job_id, job_changes)
        temp = BaseIsUpdated(**updated_job.dict())
        return temp if updated_job else BaseIsUpdated(**{"is_deleted": False})
    except Exception:
        HTTPException(status_code=500, detail="Something went wrong")


@router.post("/jobs/delete/{job_id}", response_model=BaseIsDeleted)
async def job_delete_by_id(job_id: int):
    job_collection = JobsCollection()
    try:
        deleted_job = await job_collection.delete_by_id(job_id)
        return (
            BaseIsDeleted(**deleted_job.dict())
            if deleted_job
            else BaseIsDeleted(**{"is_deleted": False})
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
