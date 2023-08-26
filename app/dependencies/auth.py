from datetime import datetime, timedelta
from typing import Annotated, Optional, List, Callable, Sequence, Any

from fastapi import HTTPException, Depends, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

from app.dependencies.db import MongoDatabase, get_database
from app.models.auth import TokenData
from app.models.user import User, UserInDb

SECRET_KEY = "ac0080731a19767803692c08a6eb437e7f60ac6bbca10a4b3ceb77fdf5190bae"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_MINUTES = 30


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="/api/v1/auth/access",
        scopes={"read": "Read information.", "write": "Write information.", "secret": "For secret info."},
    )

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def authenticate_user(self, db: MongoDatabase, email: str, password: str):
        user = self.get_user(db, email)
        if not self.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Invalid password')
        return user

    @staticmethod
    def get_user(db: MongoDatabase, email: str) -> UserInDb:
        users = db.client.get_database("mt-services")["users"]
        user_dict = users.find_one({"email": email})
        if user_dict is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")

        return UserInDb(**user_dict)

    @staticmethod
    def encode_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def encode_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(
            self,
            security_scopes: SecurityScopes,
            token: Annotated[str, Depends(oauth2_scheme)],
            db: Optional[MongoDatabase] = Depends(get_database)
    ) -> User:
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, email=email)
        except (JWTError, ValidationError):
            raise credentials_exception
        user = self.get_user(db, email=token_data.email)
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


class UserWithRole:
    auth = Auth()

    def __init__(self, roles: Optional[Sequence[str]]):
        self.roles = roles or []

    def __call__(self, user: Annotated[User, Security(auth.get_current_user, scopes=['read'])]) -> True:
        if not self.roles:
            return user
        if user.role not in self.roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient access rights")

        return user
