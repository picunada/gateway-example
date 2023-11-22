from typing import Annotated, Mapping

from fastapi import APIRouter, Depends, HTTPException

from src.auth.dependencies import UserWithRole
from src.schemas import PaginatedResponse
from src.subscription.schemas import SubscriptionOut, SubscriptionIn
from src.subscription.service import SubscriptionService
from src.user.schemas import Roles, UserInDb

router44 = APIRouter()
router223 = APIRouter()


@router44.get("/")
def list_subscriptions_44(
    service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin, Roles.default]))],
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[SubscriptionOut]:
    print(user.role)
    if user.role == Roles.admin:
        result, err = service.get_all(44, page, limit)
    else:
        result, err = service.get_all_own(44, str(user.id), page, limit)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.get("/{subscription_id}")
def get_one_subscription_44(
    service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    subscription_id: str,
) -> SubscriptionOut:
    result, err = service.get_one(44, subscription_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.post("/")
def create_subscription_44(
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin, Roles.default]))],
    service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    subscription_in: SubscriptionIn,
) -> SubscriptionOut:
    result, err = service.create(str(user.id), 44, subscription_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.put("/{subscription_id}")
def update_subscription_44(
    service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    subscription_id: str,
    subscription_in: SubscriptionIn,
) -> SubscriptionOut:
    result, err = service.update(44, subscription_id, subscription_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.delete("/{subscription_id}")
def delete_subscription_44(
    service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    subscription_id: str,
) -> Mapping[str, str]:
    result, err = service.delete(44, subscription_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.get("/")
def list_subscriptions_223(
    service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin, Roles.default]))],
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[SubscriptionOut]:
    print(user.role)
    if user.role == Roles.admin:
        result, err = service.get_all(223, page, limit)
    else:
        result, err = service.get_all_own(223, str(user.id), page, limit)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.get("/{subscription_id}")
def get_one_subscription_223(
    service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    subscription_id: str,
) -> SubscriptionOut:
    result, err = service.get_one(223, subscription_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.post("/")
def create_subscription_223(
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin, Roles.default]))],
    service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    subscription_in: SubscriptionIn,
) -> SubscriptionOut:
    print(subscription_in.model_dump(by_alias=True))
    result, err = service.create(str(user.id), 223, subscription_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.put("/{subscription_id}")
def update_subscription_223(
    service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    subscription_id: str,
    subscription_in: SubscriptionIn,
) -> SubscriptionOut:
    result, err = service.update(44, subscription_id, subscription_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.delete("/{subscription_id}")
def delete_subscription_223(
    service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    subscription_id: str,
) -> Mapping[str, str]:
    result, err = service.delete(44, subscription_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result
