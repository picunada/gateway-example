from typing import List, Union

from pydantic import BaseModel, Field

from app.models.common import PyObjectId


class ReportField(BaseModel):
    name: str
    path: Union[str, List[str]]
    type: str
    description: str


class ReportIn(BaseModel):
    name: str
    active: bool | None = False
    query: str
    fields: List[ReportField]
    title: str | None = None
    fieldsOrder: List[str] | str | None = []
    collection: str
    db: str
    subQuery: str | None = None
    subCollection: str | None = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "examples": [
                {
                    "name": "test",
                    "active": "true",
                    "db": "test",
                    "collection": "test",
                    "query": '{"$and": [{"loadDate": {"$gte": startDate}}, {"loadDate": {"$lt": endDate}}]}',
                    "fields": [
                        {
                            "name": "regNum",
                            "path": "regNum",
                            "type": "str",
                            "description": "Регистрационный номер контракта",
                        },
                    ],
                    "title": "Предметы контрактов",
                    "subCollection": "",
                }
            ]
        },
    }


class ReportOut(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    active: bool | None = False
    query: str
    fields: List[ReportField]
    title: str | None = None
    fieldsOrder: List[str] | str | None = []
    collection: str
    db: str
    subQuery: str | None = None
    subCollection: str | None = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "examples": [
                {
                    "_id": "6323593369effe25379427ff",
                    "name": "contract_44",
                    "active": "true",
                    "db": "contracts44",
                    "collection": "contractActualInfo",
                    "query": '{"$and": [{"loadDate": {"$gte": startDate}}, {"loadDate": {"$lt": endDate}}]}',
                    "fields": [
                        {
                            "name": "regNum",
                            "path": "regNum",
                            "type": "str",
                            "description": "Регистрационный номер контракта",
                        },
                    ],
                    "title": "Предметы контрактов",
                    "subCollection": "",
                }
            ]
        },
    }
