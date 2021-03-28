import boto3

from koala.aws.constants import (
    SNS_TOPIC_ARN,
    POST_CREATE,
    POST_LIKE,
    POST_COMMENT,
    FOLLOW_USER,
)
from koala.aws.services.SNS.sns import SnsWrapper


def message_producer(event, detail) -> any:
    sns_wrapper = SnsWrapper(boto3.client("sns"))

    message_group = None
    attributes = None
    if event == POST_CREATE:
        message_group = attributes = POST_CREATE
    elif event == POST_LIKE:
        message_group = attributes = POST_LIKE
    elif event == POST_COMMENT:
        message_group = attributes = POST_COMMENT
    elif event == FOLLOW_USER:
        message_group = attributes = FOLLOW_USER

    if message_group is not None and attributes is not None:
        publish_id = sns_wrapper.publish_message(
            topic_arn=SNS_TOPIC_ARN,
            message_group=message_group,
            message=detail,
            attributes=attributes,
        )
        return publish_id
