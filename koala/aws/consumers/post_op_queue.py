import json
import logging


from koala.aws.constants import POST_OP_QUEUE
from koala.aws.services.SQS.sqs import SqsWrapper
from koala.cache.posts.main import cache_create_post


async def post_consumer() -> any:
    """
    Usage:
        post_consumer(
            event=POST_CREATE
        )
    :return:
    """
    sqs_wrapper = SqsWrapper(POST_OP_QUEUE)

    try:
        sqs_messages = sqs_wrapper.receive_messages(queue=POST_OP_QUEUE)
        for msg in sqs_messages:
            msg_body = json.loads(msg.body)
            message = json.loads(msg_body.get("Message"))
            await cache_create_post(message=message)
            logging.info("Received message: %s: %s", msg.message_id, msg.body)

            # Finally, Delete messages from the queue
            # for msg in sqs_messages:
            #     sqs_wrapper.delete_message(msg)

    except Exception:
        logging.exception("Couldn't receive messages from queue: %s", POST_OP_QUEUE)
