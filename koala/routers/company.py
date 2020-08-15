import logging

from fastapi import APIRouter, HTTPException
from koala.crud.company import CompanyCollection
from pydantic import EmailStr

router = APIRouter()


@router.post("/company/get_details")
async def get_company_details(contact_email: EmailStr):
    try:
        company_collection = CompanyCollection()
        company_details = await company_collection.find_by_email(contact_email)
        return company_details
    except Exception:
        logging.info(f"Something went wrong while fetching company details")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while fetching company details",
        )
