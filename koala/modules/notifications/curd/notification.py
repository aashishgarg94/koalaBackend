import logging
from pyfcm import FCMNotification

API_KEY = "AAAA-fbXQUY:APA91bHc_r96dsYSkR4H4mzaUutNXnnW4nXRgM5AGhMsOxTV6TChT15e27aLZ8sgHdwGOIb_goPC9x1zYItZKbNyqrHiWvjPMi2JhDtHQGiShdLYkAwOPBUINthqgBuqZquDavWrGV_Q"


class Notifications:
    @staticmethod
    async def send_notifications(fcm_tokens: list) -> any:
        try:
            push_service = FCMNotification(api_key=API_KEY)

            message_title = "Pragaty notification"
            message_body = "Long time no notification from pragaty"

            result = push_service.notify_multiple_devices(
                registration_ids=fcm_tokens,
                message_title=message_title,
                message_body=message_body,
            )

            print(result)
            return True
        except Exception as e:
            logging.error(f"Error: while saving device details - {e}")
