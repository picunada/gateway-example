from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.schemas import PyObjectId


class SubscriptionIn(BaseModel):
    report_id: str = Field(alias="reportId")
    entry_key: str = Field(alias="entryKey")
    timedelta: int = Field(alias="timedelta", default=1)
    last_run: Optional[datetime] = Field(alias="lastRun", default=None)
    last_successful_run: Optional[datetime] = Field(
        alias="lastSuccessfulRun", default=None
    )


class SubscriptionOut(BaseModel):
    model_config = {"arbitrary_types_allowed": True, "populate_by_name": True}
    id: PyObjectId = Field(alias="_id")
    report_id: str = Field(alias="reportId")
    entry_key: str = Field(alias="entryKey")
    last_run: Optional[datetime] = Field(alias="lastRun", default=None)
    last_successful_run: Optional[datetime] = Field(
        alias="lastSuccessfulRun", default=None
    )
