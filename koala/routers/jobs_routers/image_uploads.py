import logging

import boto3
from fastapi import APIRouter, File, HTTPException, Security, UploadFile
from koala.authentication.authentication_company import get_current_active_user_company
from koala.authentication.authentication_user import get_current_active_user
from koala.constants import S3_IMAGE_BUCKET_COMPANY_BANNER, S3_IMAGE_BUCKET_PROFILE
from koala.crud.jobs_crud.company import CompanyCollection
from koala.crud.jobs_crud.user import MongoDBUserDatabase
from koala.models.jobs_models.user import UserInModel, UserModel
from koala.utils.utils import (
    delete_s3_resource,
    generate_unique_name,
    get_s3_resource_url,
    upload_files,
)

router = APIRouter()

s3_client = boto3.client("s3")


@router.post(
    "/applicant_profile_image",
    dependencies=[Security(get_current_active_user, scopes=["applicant:write"])],
)
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["applicant:write"],
    ),
):
    try:
        object_name = generate_unique_name(name_type="app-pro-img")
        s3_resource_url = get_s3_resource_url(
            bucket_name=S3_IMAGE_BUCKET_PROFILE, object_name=object_name
        )

        s3_upload = await upload_files(
            upload_file=file, bucket=S3_IMAGE_BUCKET_PROFILE, object_name=object_name
        )
        if s3_upload is True:
            logging.info(current_user)
            user_db = MongoDBUserDatabase(UserInModel)
            user_update_result = await user_db.update_profile_image_path(
                user_id=current_user.id, s3_path=s3_resource_url
            )

            if user_update_result.get("is_profile_image_updated") is True:
                return {
                    "image_upload": True,
                    "image_url": s3_resource_url,
                }
            else:
                delete_s3_resource(
                    bucket_name=S3_IMAGE_BUCKET_PROFILE, object_name=object_name
                )

        return {"image_upload": False}
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while uploading applicant profile image",
        )


@router.post(
    "/company_user_profile_image",
    dependencies=[Security(get_current_active_user_company, scopes=["company:write"])],
)
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: UserModel = Security(
        get_current_active_user_company,
        scopes=["company:write"],
    ),
):
    try:
        object_name = generate_unique_name(name_type="com-pro-img")
        s3_resource_url = get_s3_resource_url(
            bucket_name=S3_IMAGE_BUCKET_PROFILE, object_name=object_name
        )

        s3_upload = await upload_files(
            upload_file=file, bucket=S3_IMAGE_BUCKET_PROFILE, object_name=object_name
        )
        if s3_upload is True:
            logging.info(current_user)
            company_collection = CompanyCollection()
            user_update_result = await company_collection.update_profile_image_path(
                user_id=current_user.id, s3_path=s3_resource_url
            )

            if user_update_result.get("is_profile_image_updated") is True:
                return {
                    "image_upload": True,
                    "image_url": s3_resource_url,
                }
            else:
                delete_s3_resource(
                    bucket_name=S3_IMAGE_BUCKET_PROFILE, object_name=object_name
                )

        return {"image_upload": False}
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while uploading company profile image",
        )


@router.post(
    "/company_banner",
    dependencies=[Security(get_current_active_user_company, scopes=["company:write"])],
)
async def upload_company_banner_image(
    file: UploadFile = File(...),
    current_user: UserModel = Security(
        get_current_active_user_company,
        scopes=["company:write"],
    ),
):
    try:
        object_name = generate_unique_name(name_type="com-bann")
        s3_resource_url = get_s3_resource_url(
            bucket_name=S3_IMAGE_BUCKET_COMPANY_BANNER, object_name=object_name
        )

        s3_upload = await upload_files(
            upload_file=file,
            bucket=S3_IMAGE_BUCKET_COMPANY_BANNER,
            object_name=object_name,
        )
        if s3_upload is True:
            logging.info(current_user)
            company_collection = CompanyCollection()
            user_update_result = await company_collection.update_banner_image_path(
                user_id=current_user.id, s3_path=s3_resource_url
            )

            if user_update_result.get("is_company_banner_updated") is True:
                return {
                    "banner_upload": True,
                    "banner_url": s3_resource_url,
                }
            else:
                delete_s3_resource(
                    bucket_name=S3_IMAGE_BUCKET_COMPANY_BANNER, object_name=object_name
                )

        return {"banner_upload": False}
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=500, detail="Something went wrong while uploading banner image"
        )
