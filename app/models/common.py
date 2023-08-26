from typing import Any, Generic, TypeVar, Optional, List
from typing import Annotated, Union
from bson import ObjectId
from pydantic import PlainSerializer, AfterValidator, WithJsonSchema, BaseModel, Field

DataT = TypeVar('DataT')


class PaginatedResponse(BaseModel, Generic[DataT]):
    page: int = Field(title="Current page")
    count: int = Field(title="Count on this page")
    total: int = Field(title="Total count")
    results: Optional[List[DataT]] = []


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]
