from datetime import timedelta
from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import Auth
from app.dependencies.db import get_database, MongoDatabase
from app.models.auth import Token

router = APIRouter()

auth = Auth()


@router.post("/access")
def access(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Optional[MongoDatabase] = Depends(get_database)
) -> Token:
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    access_token = auth.encode_access_token(
        data={"sub": user.email, "scopes": form_data.scopes},
    )
    refresh_token = auth.encode_refresh_token(
        data={"sub": user.email, "scopes": form_data.scopes},
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh")
def refresh() -> Token:
    return
