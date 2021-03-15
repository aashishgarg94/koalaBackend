from fastapi import APIRouter, Depends, HTTPException, Security
from koala.authentication.authentication_user import get_current_active_user
from koala.models.jobs_models.user import UserModel
from koala.modules.social.posts.crud.coments import Comments
from koala.modules.social.posts.models.coments import BasePostCommentsModel

router = APIRouter()


@router.post(
    "/comment_post",
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def post_comment(
    post_id: str,
    comment: str,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        comment_details = BasePostCommentsModel(
            user_id=current_user.id, comment=comment
        )

        comments = Comments()
        post_id = await comments.comment_post(
            post_id=post_id, comment_details=comment_details
        )
        if post_id:
            return {"status_code": 200, "post_id": str(post_id.get("_id"))}
        elif post_id is None:
            return {"status_code": 404, "error": {"msg": "Post Not Found"}}
        else:
            return {"status_code": 503, "error": {"msg": "Not able to comment on post"}}

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
