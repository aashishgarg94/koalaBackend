from datetime import datetime

from koala.modules.social.posts.models.posts import (
    BasePostInModel,
    BasePostModel,
    BasePostUpdateModel,
)


def mapper_create_post(post_details: BasePostModel, media_url: str):
    post_details.media_url = media_url
    post_in_dict = BasePostInModel(**post_details.dict())

    return post_in_dict


def mapper_update_post(post_details: BasePostUpdateModel, media_url: str):
    if post_details.media_url is None:
        post_details.media_url = media_url
    post_details.updated_at = datetime.utcnow()

    return post_details
