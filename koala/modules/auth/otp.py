from datetime import datetime

from fastapi import APIRouter, HTTPException

from koala.modules.auth.curd.otp import OTP
from koala.modules.auth.utils.constants import COUNTRY_CODE, OTP_DIGIT
from koala.crud.jobs_crud.master import MasterCollections
from koala.modules.auth.utils.telesign import telesign_generate_otp, telesign_send_otp

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
        phone_number = f"{COUNTRY_CODE}{mobile_number}"
        verify_code = await telesign_generate_otp(OTP_DIGIT)

        otp = OTP()
        await otp.save_by_phone_number(
            phone_number=phone_number, verify_code=verify_code
        )

        response = await telesign_send_otp(
            phone_number=phone_number, verify_code=verify_code
        )

        if response.get('status_code') == 200:
            return {"status_code": 200, "data": {"otp_sent": True}}
        return {"status_code": 500, "error": {"msg": "Error while sending OTP"}}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Not able to generate OTP")


@router.get("/t_verify_otp")
async def t_verify_otp(mobile_number: str, verify_otp: int):
    try:
        phone_number = f"{COUNTRY_CODE}{mobile_number}"

        otp = OTP()
        data = await otp.get_by_phone_number(phone_number=phone_number)

        if data is None:
            return {"status_code": 404, "error": {"msg": "Mobile number not found"}}

        is_token_valid = datetime.now() < data.get("expired_at")
        if not is_token_valid:
            return {"status_code": 401, "error": {"msg": "OTP expired"}}
        elif verify_otp != data.get("generated_otp"):
            return {"status_code": 401, "error": {"msg": "Invalid OTP"}}
        elif verify_otp == data.get("generated_otp") and is_token_valid:
            # No assignment on below query as it's just updating the db, will push it to kafka later
            await otp.update_by_phone_number(phone_number=phone_number)
            return {"status_code": 200, "data": {"otp_verified": True}}
        else:
            return {"status_code": 500, "error": {"msg": "OTP verification failed"}}

    except Exception:
        raise HTTPException(status_code=500, detail="Not able to generate OTP")
