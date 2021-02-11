import boto3

import logging
from botocore.exceptions import ClientError

from koala.aws.constants import MAX_NUMBER, WAIT_TIME, VISIBILITY_TIMEOUT

sqs = boto3.resource("sqs")


class SqsWrapper:
    def __init__(self, sqs_queue):
        self.sqs_queue = sqs.Queue(sqs_queue)

    def receive_messages(self, queue):
        try:
            messages = self.sqs_queue.receive_messages(
                MessageAttributeNames=["All"],
                MaxNumberOfMessages=MAX_NUMBER,
                WaitTimeSeconds=WAIT_TIME,
                VisibilityTimeout=VISIBILITY_TIMEOUT,
            )
        except ClientError as error:
            logging.exception("Couldn't receive messages from queue: %s", queue)
            raise error
        else:
            return messages

    @staticmethod
    def delete_message(message):
        try:
            message.delete()
            logging.info("Deleted message: %s", message.message_id)
        except ClientError as error:
            logging.exception("Couldn't delete message: %s", message.message_id)
            raise error
