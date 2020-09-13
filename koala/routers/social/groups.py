import logging

from fastapi import APIRouter, HTTPException
from koala.crud.social.groups import SocialGroupsCollection

router = APIRouter()


# Get all gigs
@router.post("/group/create", response_model=dict)
async def create_group(group_details: dict):
    try:
        logging.info(group_details)
        master_collection = SocialGroupsCollection()
        data = await master_collection.create_group(group_details=group_details)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/group/get_all", response_model=dict)
async def get_all_groups(group_id: str):
    try:
        master_collection = SocialGroupsCollection()
        data = await master_collection.get_all_groups(group_id)
        logging.info(data)
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
