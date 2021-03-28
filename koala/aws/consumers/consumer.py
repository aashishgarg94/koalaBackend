from fastapi import APIRouter, HTTPException, Security
from koala.authentication.authentication_user import get_current_active_user
from koala.aws.consumers.post_op_queue import message_consumer

router = APIRouter()


@router.post(
    "/post_op",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def post_op():
    try:
        await message_consumer()
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
