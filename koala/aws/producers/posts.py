import boto3

from koala.aws.constants import (
    POST_CREATE,
    POST_UPDATE,
    POST_DELETE,
    SNS_TOPIC_ARN,
)
from koala.aws.services.SNS.sns import SnsWrapper


def post_producer(event, detail) -> any:
    sns_wrapper = SnsWrapper(boto3.client("sns"))

    if event == POST_CREATE:
        publish_id = sns_wrapper.publish_message(
            topic_arn=SNS_TOPIC_ARN,
            message_group=POST_CREATE,
            message=detail,
            attributes=POST_CREATE,
        )
        return publish_id
    elif event == POST_UPDATE:
        publish_id = sns_wrapper.publish_message(
            topic_arn=SNS_TOPIC_ARN,
            message_group=POST_UPDATE,
            message=detail,
            attributes=POST_UPDATE,
        )
        return publish_id
    elif event == POST_DELETE:
        publish_id = sns_wrapper.publish_message(
            topic_arn=SNS_TOPIC_ARN,
            message_group=POST_DELETE,
            message=detail,
            attributes=POST_DELETE,
        )
        return publish_id
