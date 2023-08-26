from datetime import datetime
import re
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.common import PyObjectId


class Roles(str, Enum):
    admin = "admin"
    default = "default"


class User(BaseModel):
    email: str = Field(description="Email")
    username: str = Field(description="Username")
    first_name: str | None = Field(description="First name", default='')
    last_name: str | None = Field(description="Last name", default='')


    @field_validator('email')
    @classmethod
    def validate_email(cls, email: str) -> str:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if not re.fullmatch(regex, email):
            raise ValueError("Not valid email")

        return email


class UserIn(User):
    password: str = Field(description="Password", min_length=6)
    password2: str = Field(description="Repeat password", min_length=6)

    @field_validator('email')
    @classmethod
    def validate_email(cls, email: str) -> str:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if not re.fullmatch(regex, email):
            raise ValueError("Not valid email")

        return email

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserIn':
        pw1 = self.password
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('Passwords do not match')
        return self


class UserInDb(User):
    model_config = {
        "arbitrary_types_allowed": True
    }

    id: PyObjectId | None = Field(alias="_id", default=None)
    role: Roles = Roles.default
    is_active: bool = Field(default=True)
    date_joined: datetime = Field(default=datetime.now())
    hashed_password: str = Field(description="Hashed password")