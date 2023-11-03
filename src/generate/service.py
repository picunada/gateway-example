import os
from typing import Any, Dict, Optional, Tuple

import requests


class GenerateService:
    @staticmethod
    def generate_one(
        settings: Dict[str, Any]
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Tuple[int, dict]]]:
        response = requests.post(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/generate/one", json=settings
        )

        if response.status_code == 201:
            result = response.json()
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def generate_scheduled(
        settings: Dict[str, Any]
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Tuple[int, dict]]]:
        response = requests.post(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/generate/schedule", json=settings
        )

        if response.status_code == 201:
            result = response.json()
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def stop_schedule(
        key: str,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Tuple[int, dict]]]:
        response = requests.post(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/generate/stop?key={key}"
        )

        if response.status_code == 200:
            result = response.json()
        else:
            return None, (response.status_code, response.json())

        return result, None
