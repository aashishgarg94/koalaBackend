import logging


from koala.cache.feed.curd.feed import CacheFeedPosts
from koala.cache.posts.curd.posts import CacheUserPosts
from koala.modules.devices.curd.device import UserDevices
from koala.modules.notifications.curd.notification import Notifications


async def cache_create_post(message: dict):
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

        # 1. Cache User Posts
        cache_user_posts = CacheUserPosts()
        await cache_user_posts.upsert_cache_user_posts(
            user_id=owner_id, post_id=post_id
        )

        # 2. Cache Feed Posts
        # 2.1. Get user followers
        cache_feed_posts = CacheFeedPosts()
        followers_list = await cache_feed_posts.find_user_followers(user_id=owner_id)

        # 2.2. Update feed for all followers
        await cache_feed_posts.upsert_cache_feed_posts(
            user_id=owner_id, post_id=post_id, followers_list=followers_list
        )

        # 3. Send Notification
        # 3.1. Get Device IDs for all followers
        user_devices = UserDevices()
        fcm_tokens = await user_devices.get_fcm_tokens(user_ids=followers_list)

        # 3.2. Send Notifications

        message_title = "Pragaty"
        message_body = "New post added"
        notification = Notifications()
        await notification.send_notifications(
            fcm_tokens=fcm_tokens,
            notification_title=message_title,
            notification_body=message_body,
        )

        # # 3. Cache Trending Posts
        # # 2.3. Update Trending feed based on this post weightage(Currently just dumping it in the treding feed)
        # await cache_feed_posts.upsert_cache_trending_posts(
        #     user_id=owner_id, post_id=post_id, following_list=following_list
        # )
        #
        # # 4. Send Notification
        # # 4.1. Get Device IDs for all followers
        # user_devices = UserDevices()
        # fcm_tokens = await user_devices.get_fcm_tokens(following_list)
        #
        # # 4.2. Send notifications to all devices
        # notifications = Notifications()
        # notifications_status = await notifications.send_notifications(fcm_tokens)

    except Exception as e:
        logging.info(e)
