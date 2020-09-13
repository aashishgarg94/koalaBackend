import logging

from fastapi import APIRouter, HTTPException
from koala.crud.social.users import SocialUsersCollection

router = APIRouter()


@router.post("/user/create_post", response_model=dict)
async def create_post(post_details: dict):
    try:
        logging.info(post_details)
        master_collection = SocialUsersCollection()
        data = await master_collection.create_group(post_details=post_details)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/user/all_posts", response_model=dict)
async def get_user_all_posts(user_id: str):
    try:
        master_collection = SocialUsersCollection()
        data = await master_collection.get_user_all_posts(user_id)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/user/post_by_id", response_model=dict)
async def get_user_post_by_id(post_id: str):
    try:
        logging.info(post_id)
        master_collection = SocialUsersCollection()
        data = await master_collection.get_user_post_by_id(post_id=post_id)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/user/follow_group", response_model=dict)
async def make_user_follow_group(user_details: dict):
    try:
        logging.info(user_details)
        master_collection = SocialUsersCollection()
        data = await master_collection.make_user_follow_group(user_details=user_details)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/user/followed_groups", response_model=dict)
async def get_user_followed_groups(user_id: str):
    try:
        logging.info(user_id)
        master_collection = SocialUsersCollection()
        data = await master_collection.get_user_followed_groups(user_id=user_id)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/user/follower", response_model=dict)
async def get_user_follower(user_id: str):
    try:
        logging.info(user_id)
        master_collection = SocialUsersCollection()
        data = await master_collection.get_user_follower(user_id=user_id)
        logging.info(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
