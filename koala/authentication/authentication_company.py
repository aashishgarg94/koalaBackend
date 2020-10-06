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
from pydantic import EmailStr, ValidationError

from ..authentication.jwt_handler import TokenData, pwd_context
from ..constants import ALGORITHM, SECRET_KEY
from ..crud.jobs_crud.company import CompanyCollection
from ..models.jobs_models.jobs import CompanyInPasswordModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/company")


def verify_password_company(plain_password, hashed_password):
    data = pwd_context.verify(plain_password, hashed_password)
    return data


async def authenticate_company(credentials: OAuth2PasswordRequestForm):
    user_db = CompanyCollection()
    user = await user_db.find_by_email(
        EmailStr(credentials.username), is_hashed_password_required=True
    )

    if not user:
        return False

    if not verify_password_company(credentials.password, user.hashed_password):
        return False

    # Applicant scopes
    scopes = ["company:read", "company:write", "company:delete"]
    return user, scopes


async def get_current_user_company(
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
        username: str = payload.get("email")
        if username is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except (PyJWTError, ValidationError):
        raise credentials_exception

    user_db = CompanyCollection()
    user = await user_db.find_by_email(EmailStr(token_data.username), is_hashed_password_required=True)

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


async def get_current_active_user_company(
    current_user: CompanyInPasswordModel = Depends(get_current_user_company),
):
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
