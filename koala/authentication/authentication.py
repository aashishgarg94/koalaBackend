import pprint

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from koala.authentication.jwt_handler import TokenData, pwd_context
from koala.constants import ALGORITHM, SECRET_KEY
from koala.crud.user import MongoDBUserDatabase
from koala.models.user import UserDB, UserModal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate(credentials: OAuth2PasswordRequestForm):
    user_db = MongoDBUserDatabase(UserDB)
    user = await user_db.get_by_email(credentials.username)

    if not user:
        return False
    if not verify_password(credentials.password, user.hashed_password):
        return False

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("email")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception

    user_db = MongoDBUserDatabase(UserDB)
    user = await user_db.get_by_email(token_data.username)

    if user is None:
        pprint.pprint(token_data)
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModal = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
