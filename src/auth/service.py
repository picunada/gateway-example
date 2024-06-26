import os
from typing import Annotated, Optional
from fastapi import HTTPException, WebSocketException, Depends
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from jose import JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

from src.database import MongoDatabase, get_database
from src.auth.schemas import TokenData, Token
from src.user.schemas import UserInDb
from src.auth.blacklist import Blacklist
from src.auth.jwt import JWT


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="/api/v1/auth/access",
        scopes={
            "read": "Read information.",
            "write": "Write information.",
            "secret": "For secret info.",
        },
    )

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def authenticate_user(self, db: MongoDatabase | None, email: str, password: str):
        user = self.get_user(db, email)
        if not self.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid password")
        return user

    async def get_current_user(
        self,
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Optional[MongoDatabase] = Depends(get_database),
    ) -> UserInDb:
        assert db is not None
        if Blacklist.is_blacklisted(db, token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Blacklisted"
            )

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
            payload = JWT.decode(token)
            email = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, email=email)
        except (JWTError, ValidationError):
            raise credentials_exception
        user = self.get_user(db, email=token_data.email)
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user

    async def get_current_ws_user(
        self,
        security_scopes: SecurityScopes,
        token: str,
        db: Optional[MongoDatabase] = Depends(get_database),
    ) -> UserInDb:
        assert db is not None
        if Blacklist.is_blacklisted(db, token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Blacklisted"
            )

        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
        credentials_exception = WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Could not validate credentials",
        )

        try:
            payload = JWT.decode(token)
            email = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, email=email)
        except (JWTError, ValidationError):
            raise credentials_exception
        user = self.get_user(db, email=token_data.email)
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user

    @staticmethod
    def get_user(db: MongoDatabase | None, email: str | None) -> UserInDb:
        assert db is not None
        assert email is not None

        users = db.client.get_database("mt-services")[
            f"users:{os.getenv('UVICORN_ENV')}"
        ]
        user_dict = users.find_one({"email": email})
        if user_dict is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
            )

        return UserInDb(**user_dict)

    @staticmethod
    def refresh_tokens(db: MongoDatabase | None, token: Token) -> Token:
        """Refresh tokens"""
        assert db is not None
        # Check if tokens blacklisted
        if Blacklist.is_blacklisted(
            db, token.refresh_token
        ) or Blacklist.is_blacklisted(db, token.access_token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Blacklisted"
            )
        try:
            payload = JWT.decode(token.refresh_token)
            if not payload["sub"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not valid refresh token",
                )

            users = db.client.get_database("mt-services")[
                f"users:{os.getenv('UVICORN_ENV')}"
            ]
            user_data = users.find_one({"email": payload["sub"]})
            if not user_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not valid refresh token",
                )
            user = UserInDb.model_validate(user_data)
            access_token = JWT.encode_access_token(
                data={"sub": user.email, "scopes": payload["scopes"]},
            )
            refresh_token = JWT.encode_refresh_token(
                data={"sub": user.email, "scopes": payload["scopes"]},
            )

            Blacklist.blacklist_token(db, token)
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
            )
        except KeyError as err:
            print(err)
            raise HTTPException(status_code=401, detail="Invalid token.")

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired.")
