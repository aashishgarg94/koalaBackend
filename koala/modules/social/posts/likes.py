from fastapi import APIRouter, HTTPException, Security, Depends
from koala.authentication.authentication_user import get_current_active_user
from koala.aws.constants import POST_LIKE
from koala.aws.producers.producer import message_producer
from koala.modules.social.posts.crud.likes import Likes

router = APIRouter()


@router.post(
    "/like",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def like_post(
    post_id: str,
    current_user: any = Depends(get_current_active_user),
):
    try:
        like = Likes()
        updated_post_id = await like.like_post(post_id=post_id, user_id=current_user.id)
        if post_id:
            # TODO: Push post_id and user_id (user_id=current_user.id) in Queue with event_type = POST_LIKED and
            #  like it to your cache collection
            message_producer(
                event=POST_LIKE,
                detail={"post_id": str(post_id), "user_id": str(current_user.id)},
            )
            return {"status_code": 200, "post_id": str(post_id)}
        elif updated_post_id is None:
            return {"status_code": 404, "error": {"msg": "Post Not Found"}}
        else:
            return {"status_code": 503, "error": {"msg": "Not able to like post"}}

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
