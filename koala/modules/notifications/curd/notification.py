import logging


class Notifications:
    @staticmethod
    async def send_notifications(fcm_tokens: list) -> any:
        try:
            # TODO: FCS Integration will go here
            pass
        except Exception as e:
            logging.error(f"Error: while saving device details - {e}")
