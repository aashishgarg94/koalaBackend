from datetime import datetime

from fastapi import APIRouter, HTTPException

from koala.modules.auth.curd.otp import OTP
from koala.modules.auth.utils.constants import COUNTRY_CODE, OTP_DIGIT, admin_accounts
from koala.modules.auth.utils.otp import (
    telesign_generate_otp,
    telesign_send_otp,
    msg91_resend_otp,
)

router = APIRouter()


def handle_admin_accounts(phone_number: str):
    if phone_number in admin_accounts:
        return {"type": "success", "reason": "user already exists"}


async def send_otp(phone_number: str, verify_code: int):
    try:
        handle_admin_accounts(phone_number)

        response = await telesign_send_otp(
            phone_number=phone_number, verify_code=verify_code
        )
        if response.status_code == 200:
            return {"status_code": 200, "type": "success", "data": {"otp_sent": True}}

    except Exception:
        raise HTTPException(status_code=500, detail="Not able to send OTP")


async def resend_otp(phone_number: str, verify_code: int):
    try:
        handle_admin_accounts(phone_number)

        response = await msg91_resend_otp(
            phone_number=phone_number, verify_code=verify_code
        )
        if response.status_code == 200:
            return {"status_code": 200, "type": "success", "data": {"otp_sent": True}}

    except Exception:
        raise HTTPException(status_code=500, detail="Not able to resend OTP")


@router.get("/generate_otp")
async def t_generate_otp(mobile_number: str, is_resend: bool):
    try:
        phone_number = f"{COUNTRY_CODE}{mobile_number}"
        verify_code = await telesign_generate_otp(OTP_DIGIT)

        otp = OTP()
        await otp.save_by_phone_number(
            phone_number=phone_number, verify_code=verify_code
        )

        if is_resend is False:
            return await send_otp(phone_number=phone_number, verify_code=verify_code)

        if is_resend is True:
            return await resend_otp(phone_number=phone_number, verify_code=verify_code)

        return {"status_code": 500, "error": {"msg": "Error while sending OTP"}}
    except Exception:
        raise HTTPException(status_code=500, detail="Not able to generate OTP")


@router.get("/verify_otp")
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
