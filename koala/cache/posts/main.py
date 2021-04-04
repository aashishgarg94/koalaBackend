import logging
from datetime import datetime

from bson import ObjectId

from koala.cache.feed.curd.feed import CacheFeedPosts
from koala.cache.posts.curd.posts import CacheUserPosts
from koala.crud.social.coins import CoinsCollection
from koala.models.social.users import CreateCoinsModelIn
from koala.modules.devices.curd.device import UserDevices
from koala.modules.notifications.curd.notification import Notifications
from koala.modules.social.posts.crud.likes import Likes


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

        logging.info("about to perform op...")
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

        # 4. Update coins collection
        coins_collection = CoinsCollection()
        coins_details = CreateCoinsModelIn(
            user_id=ObjectId(owner_id),
            coins_reason="Post",
            coins=5,
            time_added=datetime.now(),
        )

        await coins_collection.coins_added(
            coins_details=coins_details, user_id=owner_id, coins=5
        )

        # 5. Send Notification
        # 5.1. Get Device IDs for all followers
        user_devices = UserDevices()
        fcm_tokens = await user_devices.get_fcm_tokens(user_ids=followers_list)

        # 5.2. Send Notifications
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
        logging.info("ohhhh SNAP.... Error while performing op")
        logging.info(e)


async def op_post_like(message: dict):
    """This function updates the following cache collections
    1. Get The posts from main collection and replace cache collection
    2. Update post in cache_feed_posts for user who liked the post, with relevant details.
    3. Send notification to owner about liked by someone.

    :param message:
    :return:
    """
    try:
        post_id = message.get("post_id")
        user_id = message.get("user_id")

        # 1. Get The posts from main collection and replace cache collection
        cache_user_posts = CacheUserPosts()
        """
        Reason for replace is extra processing without replacement, as the flow then will be:
        1. Check if the collection exists in cache_posts
        2. If present update the changes
        3. If not get the posts, make the necessary changes and then insert it.
        """
        post_detail = await cache_user_posts.get_post_by_post_id(post_id=post_id)
        await cache_user_posts.upsert_cache_posts(
            post_id=post_id, post_detail=post_detail
        )

        # 2. Update post in cache_feed_posts for user who liked the post, with relevant details.
        cache_feed_posts = CacheFeedPosts()
        await cache_feed_posts.update_cache_feed_post(
            user_id=user_id, post_id=post_id, is_liked=True
        )

        # 3. Send Notification
        # 3.1. Get Device IDs for all followers
        user_devices = UserDevices()
        fcm_tokens = await user_devices.get_fcm_tokens(
            user_ids=[post_detail.get("owner")]
        )

        # 3.2. Send Notifications
        message_title = "Pragaty"
        message_body = "Someone liked your post"
        notification = Notifications()
        notif_result = await notification.send_notifications(
            fcm_tokens=fcm_tokens,
            notification_title=message_title,
            notification_body=message_body,
        )
        logging.info(f"Notification send result : {notif_result}")

    except Exception as e:
        logging.info(e)


async def op_post_comment(message: dict):
    """This function updates the following cache collections
    1. Get The posts from main collection and replace cache collection
    2. Update post in cache_feed_posts for user who commented on the post, with relevant details.
    3. Send notification to owner about someone commented on the post.

    :param message:
    :return:
    """
    try:
        post_id = message.get("post_id")
        user_id = message.get("user_id")

        # 1. Get The posts from main collection and replace cache collection
        cache_user_posts = CacheUserPosts()
        """
        Reason for replace is extra processing without replacement, as the flow then will be:
        1. Check if the collection exists in cache_posts
        2. If present update the changes
        3. If not get the posts, make the necessary changes and then insert it.
        """
        post_detail = await cache_user_posts.get_post_by_post_id(post_id=post_id)
        await cache_user_posts.upsert_cache_posts(
            post_id=post_id, post_detail=post_detail
        )

        # 2. Get if post is being liked by the user earlier
        like = Likes()
        liked_details = await like.get_by_post_id_and_user_id(
            post_id=post_id, user_id=user_id
        )

        is_post_liked = False
        if liked_details is not None:
            is_post_liked = True

        # 2. Update post in cache_feed_posts for user who liked the post, with relevant details.
        cache_feed_posts = CacheFeedPosts()
        await cache_feed_posts.update_cache_feed_post(
            user_id=user_id, post_id=post_id, is_liked=is_post_liked
        )

        # 3. Send Notification
        # 3.1. Get owner Device ID
        user_devices = UserDevices()
        fcm_tokens = await user_devices.get_fcm_tokens(
            user_ids=[post_detail.get("owner")]
        )

        # 3.2. Send Notifications
        message_title = "Pragaty"
        message_body = "Someone commented on your post"
        notification = Notifications()
        notif_result = await notification.send_notifications(
            fcm_tokens=fcm_tokens,
            notification_title=message_title,
            notification_body=message_body,
        )
        logging.info(f"Notification send result : {notif_result}")

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
        user_id = message.get("user_id")
        message.get("follower")
        """
        Currently we are not doing anything with follower, we can use it later like for showing specific alerts
        and other stuff based on follower id
        """

        # 1. Send Notification
        # 1.1. Get user Device ID
        user_devices = UserDevices()
        fcm_tokens = await user_devices.get_fcm_tokens(user_ids=[ObjectId(user_id)])

        # 1.2. Send Notifications
        message_title = "Pragaty"
        message_body = "Someone just started following you"
        notification = Notifications()
        notif_result = await notification.send_notifications(
            fcm_tokens=fcm_tokens,
            notification_title=message_title,
            notification_body=message_body,
        )
        logging.info(f"Notification send result : {notif_result}")

    except Exception as e:
        logging.info(e)
