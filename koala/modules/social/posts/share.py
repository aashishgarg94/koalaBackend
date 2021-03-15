from fastapi import APIRouter, HTTPException, Security
from koala.authentication.authentication_user import get_current_active_user
from koala.modules.social.posts.crud.share import Share

router = APIRouter()


@router.post(
    "/like_share",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def like_share(
    post_id: str,
):
    try:
        share = Share()
        post_id = await share.share_post(post_id=post_id)
        if post_id:
            # TODO: Push post_id and user_id (user_id=current_user.id) in Queue with event_type = POST_SHARED and
            #  like it to your cache collection
            return {"status_code": 200, "post_id": str(post_id.get("_id"))}
        elif post_id is None:
            return {"status_code": 404, "error": {"msg": "Post Not Found"}}
        else:
            return {"status_code": 503, "error": {"msg": "Not able to share post"}}

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
