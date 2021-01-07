import logging

from telesign.util import random_with_n_digits
from telesign.messaging import MessagingClient

from koala.modules.auth.utils.constants import (
    OTP_MESSAGE,
    TELESIGN_CUSTOMER_ID,
    TELESIGN_API_KEY,
    TELESIGN_MESSAGE_TYPE,
)


async def telesign_generate_otp(digit: int) -> int:
    try:
        return random_with_n_digits(digit)
    except Exception as e:
        logging.error(f"Error: while generating OTP {e}")
        raise e


async def telesign_send_otp(phone_number: str, verify_code: int) -> any:
    try:

        message = OTP_MESSAGE.format(verify_code)

        messaging = MessagingClient(TELESIGN_CUSTOMER_ID, TELESIGN_API_KEY)
        return messaging.message(phone_number, message, TELESIGN_MESSAGE_TYPE)
    except Exception as e:
        logging.error(f"Error: while generating OTP {e}")
        raise e
