from datetime import datetime, timedelta

from koala.modules.auth.models.otp import OTPInModel
from koala.modules.auth.utils.constants import OTP_VALIDITY


def mapper_save_otp(phone_number: str, verify_code: int):
    return OTPInModel(
        phone_number=phone_number,
        generated_otp=verify_code,
        is_consumed=False,
        is_expired=False,
        expired_at=datetime.now() + timedelta(minutes=OTP_VALIDITY),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
