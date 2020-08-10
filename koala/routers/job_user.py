import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from ..authentication.authentication import get_current_active_user
from ..constants import REQUEST_LIMIT
from ..crud.job_user import JobUser
from ..models.job_user import (
    AllowedActionModel,
    BaseApplicantCount,
    BaseIsApplied,
    BaseJobApplicant,
    BaseJobCount,
    JobApplicantAction,
    JobApplicantActionOutModel,
    JobApplicantInAction,
    JobApplicantOutWithPagination,
    UserJobsOutWithPagination,
)
from ..models.master import BaseIsUpdated
from ..models.user import UserModel

router = APIRouter()


# Apply for job
@router.post("/job/apply/", response_model=BaseIsApplied)
async def job_apply(
    job_id: str, current_user: UserModel = Depends(get_current_active_user)
):
    try:
        job_user = JobUser()
        result = await job_user.apply_job(job_id, current_user)
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Error while processing request")


@router.get("/user/jobs/count", response_model=BaseJobCount)
async def user_get_user_jobs_count(
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        job_user = JobUser()
        jobs_count = await job_user.get_user_jobs_count(current_user)

        return BaseJobCount(total_jobs=jobs_count)
    except Exception as e:
        logging.error(e)
        raise e


@router.get("/user/jobs/recent")
async def user_get_user_jobs_recent(
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_recent_jobs = current_user.job_applied
        return {"recent_job_count": len(user_recent_jobs), "jobs": user_recent_jobs}
    except Exception as e:
        logging.error(e)
        raise e


# Get all applied jobs, get user from token
@router.get("/user/jobs/")
async def get_user_all_jobs(
    page_no: Optional[int] = 1,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        job_user = JobUser()
        jobs_count = await job_user.get_user_jobs_count(current_user)

        job_list = []
        if jobs_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT

            job_list = await job_user.user_get_all_jobs(
                skip, REQUEST_LIMIT, current_user
            )

        return UserJobsOutWithPagination(
            total_jobs=jobs_count, current_page=page_no, jobs=job_list
        )
    except Exception as e:
        logging.error(e)
        raise e


@router.post("/job/applicant/count", response_model=BaseApplicantCount)
async def get_job_applicant_count(job_id: str):
    try:
        job_user = JobUser()
        applicant_count = await job_user.get_job_applicants_count(job_id=job_id)

        return BaseApplicantCount(total_applicants=applicant_count)
    except Exception as e:
        logging.error(e)
        raise e


@router.get("/jobs/applicant/recent")
async def get_jos_applicant_recent(job_id: str):
    try:
        job_user = JobUser()
        recent_applicant = await job_user.job_get_recent_applicants(job_id=job_id)
        return recent_applicant
    except Exception as e:
        logging.error(e)
        raise e


# , response_model=JobApplicantOutWithPagination
@router.post("/job/applicant/")
async def get_job_all_applicants(job_info: BaseJobApplicant):
    try:
        job_user = JobUser()
        # applicant_count = await job_user.get_job_applicants_count(
        #     job_id=job_info.job_id
        # )
        #
        # applicant_list = []
        # if applicant_count > 0:
        adjusted_page_number = job_info.page_no - 1
        skip = adjusted_page_number * REQUEST_LIMIT
        applicants_map = await job_user.job_get_all_applicants(
            skip=skip, limit=REQUEST_LIMIT, job_id=job_info.job_id
        )

        applicants_map["current_page"] = job_info.page_no
        return applicants_map

        # return JobApplicantOutWithPagination(
        #     total_applicants=applicant_count,
        #     current_page=job_info.page_no,
        #     applicants=applicant_list,
        # )
    except Exception as e:
        logging.error(e)
        raise e


@router.post("/job/application/action", response_model=BaseIsUpdated)
async def job_applicant_action(
    applicant_status: AllowedActionModel, job_applicant_detail: JobApplicantAction
):
    try:
        job_user = JobUser()
        job_user_map = JobApplicantInAction(
            **job_applicant_detail.dict(), applicant_status=applicant_status.value
        )
        result = await job_user.apply_job_action(job_user_map)
        return result if result else None
    except Exception as e:
        logging.error(f"Error while applying action: ERROR: {e}")
        raise e
