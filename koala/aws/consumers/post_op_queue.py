import json
import logging

from koala.aws.constants import (
    POST_OP_QUEUE,
    POST_CREATE,
    POST_LIKE,
    POST_COMMENT,
    FOLLOW_USER,
)
from koala.aws.services.SQS.sqs import SqsWrapper
from koala.cache.posts.main import (
    op_post_like,
    op_follow_user,
    op_post_comment,
    op_post_upsert,
)


async def message_consumer() -> any:
    """
    Usage:
        message_consumer(
            event=POST_CREATE
        )
    :return:
    """
    sqs_wrapper = SqsWrapper(POST_OP_QUEUE)

    try:
        sqs_messages = sqs_wrapper.receive_messages(queue=POST_OP_QUEUE)
        for msg in sqs_messages:
            msg_body = json.loads(msg.body)

            # Get Event
            event = msg_body.get("MessageAttributes").get("event").get("Value")

            # Get Message
            message = json.loads(msg_body.get("Message"))

            # Perform Op
            if event == POST_CREATE:
                await op_post_upsert(message=message)
            elif event == POST_LIKE:
                await op_post_like(message=message)
            elif event == POST_COMMENT:
                await op_post_comment(message=message)
            elif event == FOLLOW_USER:
                await op_follow_user(message=message)

            # logging.info("Received message: %s: %s", msg.message_id, msg.body)
            # Finally, Delete messages from the queue
            # for sqs_msg in sqs_messages:
            #     sqs_wrapper.delete_message(sqs_msg)

    except Exception as e:
        logging.exception("Couldn't receive messages from queue: %s", e)
