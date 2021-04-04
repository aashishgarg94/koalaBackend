import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Security, Depends
from koala.authentication.authentication_user import get_current_active_user
from koala.cache.feed.curd.feed import CacheFeedPosts
from koala.cache.posts.curd.posts import CacheUserPosts
from koala.constants import REQUEST_LIMIT

router = APIRouter()


@router.post(
    "/feed",
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def user_cache_feed(
    page_no: Optional[int] = 1, current_user: any = Depends(get_current_active_user)
):
    try:
        user_id = current_user.id

        adjusted_page_number = page_no - 1
        skip = adjusted_page_number * REQUEST_LIMIT
        limit = REQUEST_LIMIT

        cache_feed = CacheFeedPosts()
        post_ids_with_like = await cache_feed.get_user_feed_posts_ids(
            user_id=user_id, skip=skip, limit=limit
        )

        user_feed_posts = []
        if len(post_ids_with_like) > 0:
            user_post_ids = []
            for post_ids in post_ids_with_like:
                user_post_ids.append(post_ids.get("post_id"))

            cache_user_posts = CacheUserPosts()
            user_feed_posts = await cache_user_posts.get_posts_by_post_ids(
                user_post_ids=user_post_ids
            )
            logging.info(user_feed_posts)

        if len(user_feed_posts) > 0:
            return {"status_code": 200, "posts": user_feed_posts}
        elif len(user_feed_posts) == 0:
            return {"status_code": 404, "posts": []}
        else:
            return {"status_code": 500, "error": {"msg": "Something went wrong"}}

        # if post_id:
        #     # TODO: Push post_id and user_id (user_id=current_user.id) in Queue with event_type = POST_LIKED and
        #     #  like it to your cache collection
        #     message_producer(
        #         event=POST_LIKE,
        #         detail={"post_id": str(post_id), "user_id": str(current_user.id)},
        #     )
        #     return {"status_code": 200, "post_id": str(post_id)}
        # elif updated_post_id is None:
        #     return {"status_code": 404, "error": {"msg": "Post Not Found"}}
        # else:
        #     return {"status_code": 503, "error": {"msg": "Not able to like post"}}

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
