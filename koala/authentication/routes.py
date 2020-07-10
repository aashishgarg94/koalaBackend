from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from koala.authentication.authentication import (
    authenticate_user,
    get_current_active_user,
)
from koala.authentication.jwt_handler import *
from koala.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from koala.fixtures.dummy_data import fake_users_db
from koala.models.user import UserModal

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserModal)
async def read_users_me(current_user: UserModal = Depends(get_current_active_user)):
    return current_user
