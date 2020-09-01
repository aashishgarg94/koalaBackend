import logging

from fastapi import APIRouter, HTTPException
from koala.crud.website import WebsiteCollections
from koala.models.master import BaseIsCreated

router = APIRouter()


@router.post("/website/applicant", response_model=BaseIsCreated)
async def job_create(applicant_details: dict):
    try:
        website_collection = WebsiteCollections()
        result = await website_collection.insert_applicant(
            applicant_details=applicant_details
        )
        return result
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/website/provider", response_model=BaseIsCreated)
async def job_create(applicant_details: dict):
    try:
        website_collection = WebsiteCollections()
        result = await website_collection.insert_provider(
            applicant_details=applicant_details
        )
        return result
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")
