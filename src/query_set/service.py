import os
from typing import Optional, Tuple, Mapping

import requests

from src.schemas import PaginatedResponse
from src.query_set.schemas import QuerySet, QuerySetOut


class QuerySetService:
    @staticmethod
    def get(
        law: int, page: int = 1, limit: int = 15
    ) -> Tuple[Optional[PaginatedResponse[QuerySetOut]], Optional[Tuple[int, dict]]]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/query_set/{law}/?page={page}&limit{limit}"
        )

        if response.status_code == 200:
            result = PaginatedResponse[QuerySetOut].model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def get_one(
        law: int, query_set_id: str
    ) -> Tuple[Optional[QuerySetOut], Optional[Tuple[int, dict]]]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/query_set/{law}/{query_set_id}"
        )

        if response.status_code == 200:
            result = QuerySetOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def create(
        law: int, query_set: QuerySet
    ) -> Tuple[Optional[QuerySetOut], Optional[Tuple[int, dict]]]:
        response = requests.post(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/query_set/{law}/",
            json=query_set.model_dump(),
        )

        if response.status_code == 201:
            result = QuerySetOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def update(
        law: int, query_set_id: str, query_set: QuerySet
    ) -> Tuple[Optional[QuerySetOut], Optional[Tuple[int, dict]]]:
        response = requests.put(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/query_set/{law}/{query_set_id}",
            json=query_set.model_dump(),
        )

        if response.status_code == 200:
            result = QuerySetOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def delete(
        law: int, query_set_id: str
    ) -> Tuple[Optional[Mapping[str, str]], Optional[Tuple[int, dict]]]:
        response = requests.delete(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/query_set/{law}/{query_set_id}",
        )

        if response.status_code == 204:
            result = response.json()
        else:
            return None, (response.status_code, response.json())

        return result, None
