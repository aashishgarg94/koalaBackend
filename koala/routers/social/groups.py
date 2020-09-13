import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from koala.constants import REQUEST_LIMIT
from koala.crud.social.groups import SocialGroupsCollection
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.social.groups import (
    BaseSocialGroup,
    GroupsWithPaginationModel,
    SocialGroupCreateIn,
)

router = APIRouter()


@router.post("/group/create", response_model=BaseIsCreated)
async def create_group(group_details: BaseSocialGroup):
    try:
        master_collection = SocialGroupsCollection()
        group_details = SocialGroupCreateIn(**group_details.dict())
        return await master_collection.create_group(group_details=group_details)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/group/get_all", response_model=GroupsWithPaginationModel)
async def get_all_groups(page_no: Optional[int] = 1):
    try:
        master_collection = SocialGroupsCollection()

        groups_count = await master_collection.get_count()

        group_list = []
        if groups_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            group_list = await master_collection.get_all_groups(skip, REQUEST_LIMIT)

        return GroupsWithPaginationModel(
            total_groups=groups_count, current_page=page_no, groups=group_list
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/group/group_by_id", response_model=dict)
async def get_group_by_id(group_id: str):
    try:
        logging.info(group_id)
        master_collection = SocialGroupsCollection()
        data = await master_collection.get_group_by_id(group_id=group_id)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/group/all_users", response_model=dict)
async def get_group_users(group_id: str):
    try:
        master_collection = SocialGroupsCollection()
        data = await master_collection.get_group_users(group_id)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/group/user_by_id", response_model=dict)
async def get_group_user_by_id(user_id: str):
    try:
        logging.info(user_id)
        master_collection = SocialGroupsCollection()
        data = await master_collection.get_group_user_by_id(user_id=user_id)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
