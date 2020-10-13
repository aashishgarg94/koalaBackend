import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security
from koala.authentication.authentication_company import get_current_active_user_company
from koala.authentication.authentication_user import get_current_active_user
from koala.constants import REQUEST_LIMIT
from koala.crud.jobs_crud.jobs import JobCollection
from koala.models.jobs_models.jobs import (
    BaseJobModel,
    JobInModel,
    JobListOutWithPaginationModel,
    JobOutModel,
    JobOutWithPagination,
)
from koala.models.jobs_models.master import (
    BaseIsCreated,
    BaseIsDeleted,
    BaseIsJobClosed,
    BaseIsSaved,
    BaseIsUpdated,
)
from koala.models.jobs_models.user import UserModel

router = APIRouter()

DUMMY_COMPANY_ID = "100-workforce"


@router.post(
    "/jobs/create",
    response_model=BaseIsCreated,
    dependencies=[
        Security(
            get_current_active_user_company,
            scopes=["company:read", "company:write"],
        )
    ],
)
async def job_create(job_info: BaseJobModel):
    try:
        job_detail = JobInModel(**job_info.dict(), applicants_details={})
        job_collection = JobCollection()
        result = await job_collection.create(job_detail)
        if result is False:
            raise HTTPException(status_code=400, detail="Not able to process")
        return result
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


# USER skip AND limit for querying data. Will be used for pagination
@router.get(
    "/jobs/all/full_detail",
    response_model=JobOutWithPagination,
    dependencies=[
        Security(
            get_current_active_user_company,
            scopes=["hiring:read"],
        )
    ],
)
async def job_get_all(page_no: Optional[int] = 1):
    job_collection = JobCollection()
    try:
        jobs_count = await job_collection.get_count()

        job_list = []
        if jobs_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            job_list = await job_collection.get_all_with_full_details(
                skip, REQUEST_LIMIT
            )

        return JobOutWithPagination(
            total_jobs=jobs_count, current_page=page_no, jobs=job_list
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/jobs/all",
    response_model=JobListOutWithPaginationModel,
    dependencies=[
        Security(
            get_current_active_user_company,
            scopes=["hiring:read"],
        )
    ],
)
async def job_get_all(page_no: Optional[int] = 1):
    job_collection = JobCollection()
    try:
        jobs_count = await job_collection.get_count()

        job_list = []
        if jobs_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            job_list = await job_collection.get_all(skip, REQUEST_LIMIT)

        return JobListOutWithPaginationModel(
            total_jobs=jobs_count, current_page=page_no, jobs=job_list
        )

    except Exception as e:
        logging.error(f"Error while calling processing. Error {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")


# TODO: Get encoded job_id - Decide on encoder
@router.get(
    "/jobs/get/{job_id}",
    response_model=JobOutModel,
    dependencies=[
        Security(
            get_current_active_user_company,
            scopes=["hiring:read"],
        )
    ],
)
async def get_job_by_id(job_id: str):
    job_collection = JobCollection()
    try:
        return await job_collection.get_by_id(job_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/jobs/update/{job_id}",
    response_model=BaseIsUpdated,
    dependencies=[
        Security(
            get_current_active_user_company,
            scopes=["company:write"],
        )
    ],
)
async def job_update(job_id: str, job_detail: BaseJobModel):
    # Anything can be update regarding a job from here
    job_collection = JobCollection()
    try:
        job_changes = JobInModel(**job_detail.dict())
        updated_job = await job_collection.find_one_and_modify(job_id, job_changes)
        return BaseIsUpdated(**updated_job.dict()) if updated_job else None
    except Exception as e:
        logging.info(e)
        HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/jobs/close/{job_id}",
    response_model=BaseIsJobClosed,
    dependencies=[
        Security(
            get_current_active_user_company,
            scopes=["company:write"],
        )
    ],
)
async def job_delete_by_id(job_id: str):
    job_collection = JobCollection()
    try:
        closed_job = await job_collection.job_close_by_id(job_id)
        return (
            BaseIsJobClosed(**closed_job.dict())
            if closed_job
            else BaseIsJobClosed(**{"is_closed": False})
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/jobs/delete/{job_id}",
    response_model=BaseIsDeleted,
    dependencies=[
        Security(
            get_current_active_user_company,
            scopes=["company:write"],
        )
    ],
)
async def job_delete_by_id(job_id: str):
    job_collection = JobCollection()
    try:
        deleted_job = await job_collection.delete_by_id(job_id)
        return (
            BaseIsDeleted(**deleted_job.dict())
            if deleted_job
            else BaseIsDeleted(**{"is_deleted": False})
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/jobs/save/{job_id}",
    response_model=BaseIsSaved,
    dependencies=[
        Security(
            get_current_active_user,
            scopes=["applicant:write"],
        )
    ],
)
async def job_save_by_id(
    job_id: str, current_user: UserModel = Depends(get_current_active_user)
):
    job_collection = JobCollection()
    try:
        saved_job = await job_collection.save_job_by_id(job_id, user_id=current_user.id)
        data = (
            BaseIsSaved(id=saved_job.id, is_saved=True)
            if saved_job
            else BaseIsSaved(id=job_id, is_saved=False)
        )
        return data
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
