import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt import PyJWTError
from koala.crud.jobs_crud.user import MongoDBUserDatabase
from koala.models.jobs_models.user import UserInModel
from pydantic import ValidationError

from ..authentication.jwt_handler import TokenData, pwd_context
from ..constants import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verify_password(plain_password, hashed_password):
    data = pwd_context.verify(plain_password, hashed_password)
    return data


async def authenticate(credentials: OAuth2PasswordRequestForm):
    user_db = MongoDBUserDatabase(UserInModel)
    user = await user_db.find_by_username(credentials.username)

    if not user:
        return False

    if not verify_password(credentials.password, user.hashed_password):
        return False

    # Applicant scopes
    scopes = [
        "applicant:read",
        "applicant:write",
        "applicant:apply",
        "hiring:read",
        "social:read",
        "social:write",
    ]
    return user, scopes


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except (PyJWTError, ValidationError):
        raise credentials_exception

    user_db = MongoDBUserDatabase(UserInModel)
    user = await user_db.find_by_username(token_data.username)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: UserInModel = Depends(get_current_user),
):
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
