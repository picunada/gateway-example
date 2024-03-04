from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.blacklist import Blacklist
from src.auth.jwt import JWT
from src.auth.schemas import Token
from src.auth.service import Auth
from src.database import MongoDatabase, get_database

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
