import logging
from pyfcm import FCMNotification

API_KEY = "AIzaSyAWSdnv5O8Ai49W0FdFwYVMrq4bl7-_VvM"


class Notifications:
    @staticmethod
    async def send_notifications(fcm_tokens: list) -> any:
        try:
            push_service = FCMNotification(api_key=API_KEY)
            registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
            message_title = "Pragaty notification"
            message_body = "Long time no notification from pragaty"
            result = push_service.notify_multiple_devices(registration_ids=registration_ids,
                                                          message_title=message_title, message_body=message_body)

            print(result)
        except Exception as e:
            logging.error(f"Error: while saving device details - {e}")
