import os
from typing import Optional, Tuple, Mapping

import requests

from src.schemas import PaginatedResponse
from src.report.schemas import ReportOut, ReportIn


class ReportService:
    @staticmethod
    def get(
        law: int, page: int = 1, limit: int = 15
    ) -> Tuple[Optional[PaginatedResponse[ReportOut]], Optional[Tuple[int, dict]]]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/report{law}/?page={page}&limit{limit}"
        )

        if response.status_code == 200:
            result = PaginatedResponse[ReportOut].model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def get_one(
        law: int, id: str
    ) -> Tuple[Optional[ReportOut], Optional[Tuple[int, dict]]]:
        response = requests.get(f"{os.getenv('REPORT_SVC_ADDRESS')}/report{law}/{id}")

        if response.status_code == 200:
            result = ReportOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def create(
        law: int, report: ReportIn
    ) -> Tuple[Optional[ReportOut], Optional[Tuple[int, dict]]]:
        response = requests.post(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/report{law}/", json=report.model_dump()
        )

        if response.status_code == 201:
            result = ReportOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def update(
        law: int, id: str, report: ReportIn
    ) -> Tuple[Optional[ReportOut], Optional[Tuple[int, dict]]]:
        response = requests.put(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/report{law}/{id}",
            json=report.model_dump(),
        )

        if response.status_code == 200:
            result = ReportOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def delete(
        law: int, id: str
    ) -> Tuple[Optional[Mapping[str, str]], Optional[Tuple[int, dict]]]:
        response = requests.delete(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/report{law}/{id}",
        )

        if response.status_code == 204:
            result = response.json()
        else:
            return None, (response.status_code, response.json())

        return result, None
