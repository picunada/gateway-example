from typing import Mapping

from pydantic import BaseModel, Field

from src.schemas import PyObjectId


class Query(BaseModel):
    query: str | None = None

    params: Mapping[str, str] | None = None


class QuerySet(BaseModel):
    name: str | None = None
    description: str | None = None
    db: str | None = None
    collection: str | None = None
    queries: Mapping[str, Query] | None = None


class QuerySetOut(BaseModel):
    model_config = {"arbitrary_types_allowed": True, "populate_by_name": True}
    id: PyObjectId | None = Field(alias="_id", default=None)
    name: str | None = None
    description: str | None = None
    db: str | None = None
    collection: str | None = None
    queries: Mapping[str, Query] | None = None
