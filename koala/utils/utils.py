import logging
from datetime import datetime
from uuid import uuid4

import boto3
from fastapi import File, HTTPException, UploadFile
from koala.constants import S3_IMAGE_BUCKET_GROUPS, S3_IMAGE_BUCKET_POSTS

s3_client = boto3.client("s3")


def get_s3_resource_url(bucket_name, object_name):
    location = s3_client.get_bucket_location(Bucket=bucket_name)["LocationConstraint"]
    return "https://%s.s3.%s.amazonaws.com/%s" % (bucket_name, location, object_name)
    # return f"https://{bucket_name}.s3.{location}.amazonaws.com/{object_name}" -- keeping it for now


def delete_s3_resource(bucket_name, object_name):
    return s3_client.delete_object(Bucket=bucket_name, Key=object_name)


def generate_unique_name(name_type: str = None):
    return f"{name_type}-{datetime.now().strftime('%Y%m-%d%H-%M%S-')}{str(uuid4())}.png"


async def upload_files(upload_file, bucket, object_name):
    try:
        upload_file.file.seek(0)
        s3_client.upload_fileobj(
            upload_file.file,
            bucket,
            object_name,
            ExtraArgs={"ContentType": "image/png", "ACL": "public-read"},
        )
    except Exception as e:
        logging.error(e)
        return False
    return True


async def upload_social_post_image(file: UploadFile = File(...)):
    try:
        object_name = generate_unique_name(name_type="soc-pos-img")
        s3_resource_url = get_s3_resource_url(
            bucket_name=S3_IMAGE_BUCKET_POSTS, object_name=object_name
        )

        s3_upload = await upload_files(
            upload_file=file, bucket=S3_IMAGE_BUCKET_POSTS, object_name=object_name
        )
        if s3_upload is True:
            return {
                "is_post_image_upload": True,
                "post_image_url": s3_resource_url,
            }
        else:
            return {"is_post_image_upload": False}
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while uploading social post image",
        )


async def upload_social_group_image(file: UploadFile = File(...)):
    try:
        object_name = generate_unique_name(name_type="soc-gro-img")
        s3_resource_url = get_s3_resource_url(
            bucket_name=S3_IMAGE_BUCKET_GROUPS, object_name=object_name
        )

        s3_upload = await upload_files(
            upload_file=file, bucket=S3_IMAGE_BUCKET_GROUPS, object_name=object_name
        )
        if s3_upload is True:
            return {
                "is_group_image_upload": True,
                "group_image_url": s3_resource_url,
            }
        else:
            return {"is_group_image_upload": False}
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while uploading social post image",
        )
