from typing import Mapping, List

from pydantic import BaseModel, Field

from src.schemas import PyObjectId


class FieldPath(BaseModel):
    path: str | List[str] | None = None
    source: str | List[str] | None = None


class ReportField(BaseModel):
    description: str | None = None
    actual_path: FieldPath | List[FieldPath] | None = Field(
        alias="actualPath", default=None
    )
    path: FieldPath | List[FieldPath] | None = None


class FieldSet(BaseModel):
    name: str | None = None
    description: str | None = None
    source_set: str | None = Field(alias="sourceSet", default=None)
    fields: Mapping[str, ReportField] | None = None


class FieldSetOut(BaseModel):
    model_config = {"arbitrary_types_allowed": True, "populate_by_name": True}
    id: PyObjectId | None = Field(alias="_id", default=None)
    name: str | None = None
    description: str | None = None
    source_set: str | None = Field(alias="sourceSet", default=None)
    fields: Mapping[str, ReportField] | None = None
