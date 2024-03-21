import os
from datetime import datetime, timedelta, timezone
from enum import Enum
from http import HTTPStatus
from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from db_utils import users
from log_conf import logger


credentials_exception = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail="UNAUTHORISED: Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

try:
    # Retrieve the values of the environment variables
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
except Exception as e:
    logger.error(f"BAD environment variables: {e}")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserType(str, Enum):
    walker = "walker"
    owner = "owner"
    admin = "admin"


class User(BaseModel):
    _id: str
    username: str
    email: str | None = None
    type: UserType | None = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(users_table, username: str):
    for user in users_table.find():
        if username in user["username"]:
            return UserInDB(**user)


def authenticate_user(users_table, username: str, password: str):
    user = get_user(users_table, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    logger.info(f"User {user.username} Authenticated")
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
