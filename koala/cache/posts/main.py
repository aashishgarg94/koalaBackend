import logging

from koala.cache.feed.curd.feed import CacheFeedPosts
from koala.cache.posts.curd.posts import CacheUserPosts
from koala.modules.devices.curd.device import UserDevices
from koala.modules.notifications.curd.notification import Notifications


async def op_post_upsert(message: dict):
    """This function updates the following cache collections
    1. Cache User Posts
    2. Cache User Feed
    3. Cache Posts Trending

    :param message:
    :return:
    """
    try:
        post_id = message.get("post_id")
        owner_id = message.get("owner_id")

        # 1. Update secondary posts
        cache_user_posts = CacheUserPosts()
        # 1.1 Get Collection from Post collection
        post_detail = await cache_user_posts.get_post_by_post_id(post_id=post_id)

        # Upsert post to secondary collection
        await cache_user_posts.upsert_cache_posts(
            post_id=post_id, post_detail=post_detail
        )

        # 2. Cache User Posts
        cache_user_posts = CacheUserPosts()
        await cache_user_posts.upsert_cache_user_posts(
            user_id=owner_id, post_id=post_id
        )

        # 3. Cache Feed Posts
        # 3.1. Get user followers
        cache_feed_posts = CacheFeedPosts()
        followers_list = await cache_feed_posts.find_user_followers(user_id=owner_id)

        # 3.2. Update feed for all followers
        await cache_feed_posts.upsert_cache_feed_posts(
            post_id=post_id, followers_list=followers_list
        )

        # 4. Send Notification
        # 4.1. Get Device IDs for all followers
        user_devices = UserDevices()
        fcm_tokens = await user_devices.get_fcm_tokens(user_ids=followers_list)

        # 4.2. Send Notifications
        message_title = "Pragaty"
        message_body = "New post added"
        notification = Notifications()
        notif_result = await notification.send_notifications(
            fcm_tokens=fcm_tokens,
            notification_title=message_title,
            notification_body=message_body,
        )
        logging.info(f"Notification send result : {notif_result}")
    except Exception as e:
        logging.info(e)


async def op_post_like(message: dict):
    """This function updates the following cache collections
    1. Cache User Posts
    2. Cache User Feed
    3. Cache Posts Trending

    :param message:
    :return:
    """
    try:
        message.get("post_id")
        message.get("user_id")

        """
        1. Update cache collection with user details
        2. Update secondary post collection
        3. Send notification
        """

    except Exception as e:
        logging.info(e)


async def op_post_comment(message: dict):
    """This function updates the following cache collections
    1. Cache User Posts
    2. Cache User Feed
    3. Cache Posts Trending

    :param message:
    :return:
    """
    try:
        message.get("post_id")
        message.get("user_id")
        message.get("comment")
        message.get("commented_at")

        """
        1. Update cache collection with user details
        2. Update secondary post collection
        3. Send notification
        """

    except Exception as e:
        logging.info(e)


async def op_follow_user(message: dict):
    """This function updates the following cache collections
    1. Cache User Posts
    2. Cache User Feed
    3. Cache Posts Trending

    :param message:
    :return:
    """
    try:
        message.get("user_id")
        message.get("follower")

        """
        1. Update cache collection with user details
        2. Update secondary post collection
        3. Send notification
        """

    except Exception as e:
        logging.info(e)
