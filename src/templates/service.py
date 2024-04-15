import os
from typing import Optional, Tuple

import requests

from src.report.schemas import ReportOut
from src.schemas import PaginatedResponse


class ReportService:
    @staticmethod
    def get_all(
        law: int, page: int = 1, limit: int = 15
    ) -> Tuple[Optional[PaginatedResponse[ReportOut]], Optional[Tuple[int, dict]]]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/templates/{law}/?page={page}&limit{limit}"
        )

        if response.status_code == 200:
            result = PaginatedResponse[ReportOut].model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

   