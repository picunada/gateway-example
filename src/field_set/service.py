import os
from typing import Optional, Tuple, Mapping

import requests

from src.schemas import PaginatedResponse
from src.field_set.schemas import FieldSet, FieldSetOut


class FieldSetService:
    @staticmethod
    def get(
        law: int, page: int = 1, limit: int = 15
    ) -> Tuple[Optional[PaginatedResponse[FieldSetOut]], Optional[Tuple[int, dict]]]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/field_set/{law}/?page={page}&limit{limit}"
        )

        if response.status_code == 200:
            result = PaginatedResponse[FieldSetOut].model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def get_one(
        law: int, field_set_id: str
    ) -> Tuple[Optional[FieldSetOut], Optional[Tuple[int, dict]]]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/field_set/{law}/{field_set_id}"
        )

        if response.status_code == 200:
            result = FieldSetOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def create(
        law: int, field_set: FieldSet
    ) -> Tuple[Optional[FieldSetOut], Optional[Tuple[int, dict]]]:
        response = requests.post(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/field_set/{law}/",
            json=field_set.model_dump(),
        )

        if response.status_code == 201:
            result = FieldSetOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def update(
        law: int, field_set_id: str, field_set: FieldSet
    ) -> Tuple[Optional[FieldSetOut], Optional[Tuple[int, dict]]]:
        response = requests.put(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/field_set/{law}/{field_set_id}",
            json=field_set.model_dump(),
        )

        if response.status_code == 200:
            result = FieldSetOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def delete(
        law: int, field_set_id: str
    ) -> Tuple[Optional[Mapping[str, str]], Optional[Tuple[int, dict]]]:
        response = requests.delete(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/field_set/{law}/{field_set_id}",
        )

        if response.status_code == 204:
            result = response.json()
        else:
            return None, (response.status_code, response.json())

        return result, None
