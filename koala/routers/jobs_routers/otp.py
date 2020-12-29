from fastapi import APIRouter, HTTPException
from koala.crud.jobs_crud.master import MasterCollections
from telesign.messaging import MessagingClient
from telesign.util import random_with_n_digits
import sys

router = APIRouter()


@router.get(
    "/generate_otp",
)
async def generate_otp(mobile_number: str, is_resend: bool):
    try:
        master_collection = MasterCollections()
        return await master_collection.generate_otp(mobile_number)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/verify_otp",
)
async def generate_otp(mobile_number: str, otp: str):
    try:
        master_collection = MasterCollections()
        return await master_collection.verify_otp(mobile_number, otp)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/t_generate_otp")
async def t_generate_otp(mobile_number: str):
    try:
        customer_id = "799079BA-116B-45E8-811B-79F68268D064"
        api_key = "rEyKCONdyxeGcGbU6pEUFMyD8vf98Js6s1UgJCz87ThwoEx7mP9LTcD6vNVcF7eb+Ac0xQtIGPdbo8bVwEvkjQ=="

        country_code = '91'
        phone_number = country_code + mobile_number
        verify_code = random_with_n_digits(4)

        message = "Your code is {}".format(verify_code)
        message_type = "OTP"

        messaging = MessagingClient(customer_id, api_key)
        response = messaging.message(phone_number, message, message_type)
        return response
    except Exception:
        raise HTTPException(status_code=500, detail="Not able to generate OTP")
