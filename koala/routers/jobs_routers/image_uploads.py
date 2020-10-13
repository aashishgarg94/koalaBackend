import logging

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        # with open(file_name, "rb") as f:
        # with file_name as f:
        #     f.seek(0)
        s3_client.upload_fileobj(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return response


@router.post("/profile_image")
async def profile_image(file: UploadFile = File(...)):
    try:
        logging.info({"filename": file.filename})
        logging.info(file)
        logging.info(file.file)
        logging.info("image upload check")
        # contents = await file.read()
        # logging.info(contents)

        # s3 = boto3.resource('s3')
        # for bucket in s3.buckets.all():
        #     print(bucket.name)
        s3_upload = upload_file(file.file, "koala-profile-images")
        logging.info(s3_upload)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong while ")
