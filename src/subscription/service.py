import os
from typing import Optional, Tuple, Mapping

import requests

from src.schemas import PaginatedResponse
from src.subscription.schemas import SubscriptionOut, SubscriptionIn


class SubscriptionService:
    @staticmethod
    def get_all(
        law: int, page: int = 1, limit: int = 15
    ) -> Tuple[
        Optional[PaginatedResponse[SubscriptionOut]], Optional[Tuple[int, dict]]
    ]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/subscription/{law}/?page={page}&limit{limit}"
        )

        if response.status_code == 200:
            result = PaginatedResponse[SubscriptionOut].model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def get_all_own(
        law: int,
        user_id: str,
        page: int = 1,
        limit: int = 15,
    ) -> Tuple[
        Optional[PaginatedResponse[SubscriptionOut]], Optional[Tuple[int, dict]]
    ]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/subscription/{law}/?user_id={str(user_id)}&page={page}&limit{limit}"
        )

        if response.status_code == 200:
            result = PaginatedResponse[SubscriptionOut].model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def get_one(
        law: int, subscription_id: str
    ) -> Tuple[Optional[SubscriptionOut], Optional[Tuple[int, dict]]]:
        response = requests.get(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/subscription/{law}/{subscription_id}"
        )

        if response.status_code == 200:
            result = SubscriptionOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def create(
        user_id: str, law: int, subsciption: SubscriptionIn
    ) -> Tuple[Optional[SubscriptionOut], Optional[Tuple[int, dict]]]:
        response = requests.post(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/subscription/{law}/",
            json={**subsciption.model_dump(by_alias=True), "user_id": str(user_id)},
        )

        if response.status_code == 201:
            result = SubscriptionOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def update(
        law: int, subscription_id: str, report: SubscriptionIn
    ) -> Tuple[Optional[SubscriptionOut], Optional[Tuple[int, dict]]]:
        response = requests.put(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/subscription/{law}/{subscription_id}",
            json=report.model_dump(),
        )

        if response.status_code == 200:
            result = SubscriptionOut.model_validate(response.json())
        else:
            return None, (response.status_code, response.json())

        return result, None

    @staticmethod
    def delete(
        law: int, subscription_id: str
    ) -> Tuple[Optional[Mapping[str, str]], Optional[Tuple[int, dict]]]:
        response = requests.delete(
            f"{os.getenv('REPORT_SVC_ADDRESS')}/generate/stop/{subscription_id}",
        )

        if response.status_code == 204:
            result = response.json()
        else:
            return None, (response.status_code, response.json())

        return result, None
