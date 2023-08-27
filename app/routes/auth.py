from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import Auth
from app.dependencies.db import get_database, MongoDatabase
from app.models.auth import Token
from app.service.blacklist import Blacklist
from app.service.jwt import JWT

router = APIRouter()

auth = Auth()


@router.post("/access")
def access(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Optional[MongoDatabase] = Depends(get_database),
) -> Token:
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    access_token = JWT.encode_access_token(
        data={"sub": user.email, "scopes": form_data.scopes},
    )
    refresh_token = JWT.encode_refresh_token(
        data={"sub": user.email, "scopes": form_data.scopes},
    )
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh")
def refresh(
    token: Annotated[Token, Body()], db: Optional[MongoDatabase] = Depends(get_database)
) -> Token:
    token = auth.refresh_tokens(db, token)
    return token


@router.post("/logout")
def logout(token: Token, db: Optional[MongoDatabase] = Depends(get_database)):
    Blacklist.blacklist_token(db, token)
    return {"detail": "Logout"}
