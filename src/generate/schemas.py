from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str
    username: str
    email: str


class Schedule(BaseModel):
    minute: str | int = Field(default="*")
    hour: str | int = Field(default="*")
    day_of_week: str | int = Field(default="*")
    day_of_month: str | int = Field(default="*")
    month_of_year: str | int = Field(default="*")


class GenerateSettings(BaseModel):
    report_id: str
    params: Dict[str, Any]
