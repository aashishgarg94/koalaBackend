import logging

from fastapi import APIRouter, HTTPException
from koala.aws.consumers.post_op_queue import message_consumer

router = APIRouter()


# @router.post(
#     "/post_op",
#     dependencies=[Security(get_current_active_user, scopes=["social:write"])],
# )
@router.post("/post_op")
async def post_op():
    try:
        logging.info("post op called")
        await message_consumer()
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
