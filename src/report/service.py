import os
from typing import Optional, Tuple
from fastapi import Response, status

import requests

from src.schemas import PaginatedResponse
from src.report.schemas import ReportOut, ReportIn


class ReportService:
    @staticmethod
    def get_all(
        law: int, page: int = 1, limit: int = 15
    ) -> Tuple[Optional[PaginatedResponse[ReportOut]], Optional[Tuple[int, dict]]]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/report/{law}/?page={page}&limit{limit}"
        )

        if response.status_code == 200:
            result = PaginatedResponse[ReportOut].model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def get_all_own(
        law: int,
        user_id: str,
        page: int = 1,
        limit: int = 15,
    ) -> Tuple[Optional[PaginatedResponse[ReportOut]], Optional[Tuple[int, dict]]]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/report/{law}/?user_id={str(user_id)}&page={page}&limit{limit}"
        )

        if response.status_code == 200:
            result = PaginatedResponse[ReportOut].model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def get_one(
        law: int, report_id: str
    ) -> Tuple[Optional[ReportOut], Optional[Tuple[int, dict]]]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/report/{law}/{report_id}"
        )

        if response.status_code == 200:
            result = ReportOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def create(
        user_id: str, law: int, report: ReportIn
    ) -> Tuple[Optional[ReportOut], Optional[Tuple[int, dict]]]:
        response = requests.post(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/report/{law}/",
            json={**report.model_dump(by_alias=True), "user_id": str(user_id)},
        )

        if response.status_code == 201:
            result = ReportOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def update(
        law: int, report_id: str, report: ReportIn
    ) -> Tuple[Optional[ReportOut], Optional[Tuple[int, dict]]]:
        response = requests.put(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/report/{law}/{report_id}",
            json=report.model_dump(),
        )

        if response.status_code == 200:
            result = ReportOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def delete(
        law: int, report_id: str, user_id: str
    ) -> Tuple[Optional[Response], Optional[tuple[int, dict]]]:
        response = requests.delete(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/report/{law}/{report_id}?user_id={str(user_id)}",
        )

        if response.status_code == 204:
            return Response(status_code=status.HTTP_204_NO_CONTENT), None
        else:
            return None, (response.status_code, response.json())
