import logging
from datetime import datetime
from uuid import uuid4

import boto3
from fastapi import APIRouter, File, HTTPException, UploadFile
from koala.constants import (
    S3_IMAGE_BUCKET_COMPANY_PROFILE,
    S3_IMAGE_BUCKET_POSTS,
    S3_IMAGE_BUCKET_PROFILE,
)

router = APIRouter()

s3_client = boto3.client("s3")


def get_s3_resource_url(bucket_name, object_name):
    location = s3_client.get_bucket_location(Bucket=bucket_name)["LocationConstraint"]
    return "https://%s.s3.%s.amazonaws.com/%s" % (bucket_name, location, object_name)
    # return f"https://{bucket_name}.s3.{location}.amazonaws.com/{object_name}" -- keeping it for now


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


@router.post("/profile_image")
async def upload_profile_image(file: UploadFile = File(...)):
    try:
        object_name = generate_unique_name(name_type="profile-img")
        s3_upload = await upload_files(
            upload_file=file, bucket=S3_IMAGE_BUCKET_PROFILE, object_name=object_name
        )
        logging.info(s3_upload)
        if s3_upload is True:
            return {
                "image_upload": True,
                "image_url": get_s3_resource_url(
                    bucket_name=S3_IMAGE_BUCKET_PROFILE, object_name=object_name
                ),
            }
        else:
            return {"image_upload": False}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong while ")


@router.post("/company_profile_image")
async def upload_company_profile_image(file: UploadFile = File(...)):
    try:
        object_name = generate_unique_name(name_type="company-profile-img")
        s3_upload = await upload_files(
            upload_file=file,
            bucket=S3_IMAGE_BUCKET_COMPANY_PROFILE,
            object_name=object_name,
        )
        logging.info(s3_upload)
        if s3_upload is True:
            return {
                "image_upload": True,
                "image_url": get_s3_resource_url(
                    bucket_name=S3_IMAGE_BUCKET_COMPANY_PROFILE, object_name=object_name
                ),
            }
        else:
            return {"image_upload": False}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong while ")


async def upload_social_post_image(file: UploadFile = File(...)):
    try:
        object_name = generate_unique_name(name_type="social-post-img")
        s3_upload = await upload_files(
            upload_file=file, bucket=S3_IMAGE_BUCKET_POSTS, object_name=object_name
        )
        logging.info(s3_upload)
        if s3_upload is True:
            return {
                "image_upload": True,
                "image_url": get_s3_resource_url(
                    bucket_name=S3_IMAGE_BUCKET_POSTS, object_name=object_name
                ),
            }
        else:
            return {"image_upload": False}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong while ")
