import logging
from pyfcm import FCMNotification

API_KEY = "AAAA-fbXQUY:APA91bHc_r96dsYSkR4H4mzaUutNXnnW4nXRgM5AGhMsOxTV6TChT15e27aLZ8sgHdwGOIb_goPC9x1zYItZKbNyqrHiWvjPMi2JhDtHQGiShdLYkAwOPBUINthqgBuqZquDavWrGV_Q"


class Notifications:
    @staticmethod
    async def send_notifications(
            fcm_tokens: list, notification_title: str, notification_body: str
    ) -> bool:
        try:
            push_service = FCMNotification(api_key=API_KEY)

            message_title = notification_title
            message_body = notification_body

            result = push_service.notify_multiple_devices(
                registration_ids=fcm_tokens,
                message_title=message_title,
                message_body=message_body,
            )
            # We can use the above result to do something here if we are not able to send the push
            return True

        except Exception as e:
            logging.error(f"Error: while saving device details - {e}")
