import logging
import requests
import json

class Notifications:
    @staticmethod
    async def send_notifications(fcm_tokens: list) -> any:
        try:
            for fcm_token in fcm_tokens:
                server_token = 'your server key here'
                device_token = 'device token here'

                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + server_token,
                }

                body = {
                    'notification': {'title': 'Sending push form python script',
                                     'body': 'New Message'
                                     },
                    'to':
                        device_token,
                    'priority': 'high',
                    #   'data': dataPayLoad,
                }
                response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
                print(response.status_code)

                print(response.json())
                pass
        except Exception as e:
            logging.error(f"Error: while saving device details - {e}")
