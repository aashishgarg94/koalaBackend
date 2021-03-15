import json
import logging
from botocore.exceptions import ClientError


class SnsWrapper:
    def __init__(self, sns_client):
        self.sns_client = sns_client

    def list_topics(self):
        try:
            topics_iter = self.sns_client.list_topics()
            logging.info("Got topics.")
        except ClientError:
            logging.exception("Couldn't get topics.")
            raise
        else:
            return topics_iter

    def publish_message(self, topic_arn, message_group, message, attributes):
        try:
            att_dict = {"event": {"DataType": "String", "StringValue": f"{attributes}"}}
            response = self.sns_client.publish(
                TopicArn=topic_arn,
                MessageGroupId=message_group,
                Message=json.dumps(message),
                MessageAttributes=att_dict,
            )
            message_id = response["MessageId"]
            logging.info(
                "Published message with attributes %s to topic %s.",
                attributes,
                topic_arn,
            )
        except ClientError:
            logging.exception("Couldn't publish message to topic %s.", topic_arn)
            raise
        else:
            return message_id
