import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from koala.authentication import authentication_company, authentication_user
from koala.authentication.jwt_handler import Token, create_access_token
from koala.constants import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_user(credentials: OAuth2PasswordRequestForm = Depends()):
    try:
        user, scopes = await authentication_user.authenticate(credentials)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "username": user.username,
                "mobile_number": user.mobile_number,
                "scopes": scopes,
            },
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong while login ")


@router.post("/login/company", response_model=Token)
async def login_company(credentials: OAuth2PasswordRequestForm = Depends()):
    try:
        company, scopes = await authentication_company.authenticate_company(credentials)
        logging.info(company)
        logging.info(scopes)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "username": company.company_name,
                "email": company.contact_email,
                "scopes": scopes,
            },
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong while ")
