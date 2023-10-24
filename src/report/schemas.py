from typing import Dict

from pydantic import BaseModel, Field

from src.schemas import PyObjectId


class ReportField(BaseModel):
    name: str
    field_set: str
    field_name: str
    func: str
    type: str
    query: str


class ReportIn(BaseModel):
    name: str
    description: str
    report_params: Dict[str, str]
    queries: Dict[str, Dict[str, str | Dict[str, str]]]
    fields: Dict[str, ReportField]

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "examples": [
                {
                    "name": "purchase",
                    "description": "Закупки",
                    "reportParams": {"^startDate": "date", "^endDate": "date"},
                    "queries": {
                        "purchaseByDays": {
                            "querySet": "purchase",
                            "#startDate": "^startDate",
                            "#endDate": "^endDate",
                            "purchaseBySourceId": {
                                "querySet": "purchase",
                                "#sourceId": "~sourceId",
                                "#collection": "~collection",
                            },
                        }
                    },
                    "fields": {
                        "purchaseNumber": {
                            "fieldSet": "fieldSets223",
                            "name": "purchaseActual",
                            "fieldName": "purchaseNumber",
                            "func": "first",
                            "type": "str",
                            "query": "purchaseByDays",
                        },
                        "docPublishDate": {
                            "fieldSet": "fieldSets223",
                            "name": "purchase",
                            "fieldName": "docPublishDate",
                            "func": "first",
                    "name": "purchase",
                    "description": "Закупки",
                    "reportParams": {"^startDate": "date", "^endDate": "date"},
                    "queries": {
                        "purchaseByDays": {
                            "querySet": "purchase",
                            "#startDate": "^startDate",
                            "#endDate": "^endDate",
                            "purchaseBySourceId": {
                                "querySet": "purchase",
                                "#sourceId": "~sourceId",
                                "#collection": "~collection",
                            },
                        }
                    },
                    "fields": {
                        "purchaseNumber": {
                            "fieldSet": "fieldSets223",
                            "name": "purchaseActual",
                            "fieldName": "purchaseNumber",
                            "func": "first",
                            "type": "str",
                            "query": "purchaseByDays",
                        },
                        "docPublishDate": {
                            "fieldSet": "fieldSets223",
                            "name": "purchase",
                            "fieldName": "docPublishDate",
                            "func": "first",
                    "name": "purchase",
                    "description": "Закупки",
                    "reportParams": {
                        "^startDate": "date",
                        "^endDate": "date"
                    },
                    "queries": {
                        "purchaseByDays": {
                            "querySet": "purchase",
                            "#startDate": "^startDate",
                            "#endDate": "^endDate",
                            "purchaseBySourceId": {
                                "querySet": "purchase",
                                "#sourceId": "~sourceId",
                                "#collection": "~collection"
                            }
                        }
                    },
                    "fields": {
                        "purchaseNumber": {
                            "fieldSet": "fieldSets223",
                            "name": "purchaseActual",
                            "fieldName": "purchaseNumber",
                            "func": "first",
                            "type": "str",
                            "query": "purchaseByDays",
                        },
                        "docPublishDate": {
                            "fieldSet": "fieldSets223",
                            "name": "purchase",
                            "fieldName": "docPublishDate",
                            "func": "first",
                            "type": "str",
                            "query": "purchaseBySourceId",
                            "query": "purchaseBySourceId",
                        },
                    },
                    },
                }
            ]
        },
    }


class ReportOut(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    description: str
    report_params: Dict[str, str]
    queries: Dict[str, Dict[str, str | Dict[str, str]]]
    fields: Dict[str, ReportField]

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "examples": [
                {
                    "name": "purchase",
                    "description": "Закупки",
                    "reportParams": {"^startDate": "date", "^endDate": "date"},
                    "queries": {
                        "purchaseByDays": {
                            "querySet": "purchase",
                            "#startDate": "^startDate",
                            "#endDate": "^endDate",
                            "purchaseBySourceId": {
                                "querySet": "purchase",
                                "#sourceId": "~sourceId",
                                "#collection": "~collection",
                            },
                        }
                    },
                    "fields": {
                        "purchaseNumber": {
                            "fieldSet": "fieldSets223",
                            "name": "purchaseActual",
                            "fieldName": "purchaseNumber",
                            "func": "first",
                            "type": "str",
                            "query": "purchaseByDays",
                        },
                        "docPublishDate": {
                            "fieldSet": "fieldSets223",
                            "name": "purchase",
                            "fieldName": "docPublishDate",
                            "func": "first",
                    "name": "purchase",
                    "description": "Закупки",
                    "reportParams": {"^startDate": "date", "^endDate": "date"},
                    "queries": {
                        "purchaseByDays": {
                            "querySet": "purchase",
                            "#startDate": "^startDate",
                            "#endDate": "^endDate",
                            "purchaseBySourceId": {
                                "querySet": "purchase",
                                "#sourceId": "~sourceId",
                                "#collection": "~collection",
                            },
                        }
                    },
                    "fields": {
                        "purchaseNumber": {
                            "fieldSet": "fieldSets223",
                            "name": "purchaseActual",
                            "fieldName": "purchaseNumber",
                            "func": "first",
                            "type": "str",
                            "query": "purchaseByDays",
                        },
                        "docPublishDate": {
                            "fieldSet": "fieldSets223",
                            "name": "purchase",
                            "fieldName": "docPublishDate",
                            "func": "first",
                    "name": "purchase",
                    "description": "Закупки",
                    "reportParams": {
                        "^startDate": "date",
                        "^endDate": "date"
                    },
                    "queries": {
                        "purchaseByDays": {
                            "querySet": "purchase",
                            "#startDate": "^startDate",
                            "#endDate": "^endDate",
                            "purchaseBySourceId": {
                                "querySet": "purchase",
                                "#sourceId": "~sourceId",
                                "#collection": "~collection"
                            }
                        }
                    },
                    "fields": {
                        "purchaseNumber": {
                            "fieldSet": "fieldSets223",
                            "name": "purchaseActual",
                            "fieldName": "purchaseNumber",
                            "func": "first",
                            "type": "str",
                            "query": "purchaseByDays",
                        },
                        "docPublishDate": {
                            "fieldSet": "fieldSets223",
                            "name": "purchase",
                            "fieldName": "docPublishDate",
                            "func": "first",
                            "type": "str",
                            "query": "purchaseBySourceId",
                            "query": "purchaseBySourceId",
                        },
                    },
                    },
                }
            ]
        },
    }
