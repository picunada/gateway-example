from typing import Annotated, Mapping

from fastapi import APIRouter, Depends, HTTPException

from src.auth.dependencies import UserWithRole
from src.schemas import PaginatedResponse
from src.query_set.schemas import QuerySet, QuerySetOut
from src.user.schemas import Roles, UserInDb
from src.query_set.service import QuerySetService

router44 = APIRouter()
router223 = APIRouter()


@router44.get("/")
def list_query_set_44(
    service: Annotated[QuerySetService, Depends(QuerySetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin]))],
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[QuerySetOut]:
    result, err = service.get(44, page, limit)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.get("/{query_set_id}")
def get_one_query_set_44(
    service: Annotated[QuerySetService, Depends(QuerySetService)],
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    query_set_id: str,
) -> QuerySetOut:
    result, err = service.get_one(44, query_set_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.post("/")
def create_query_set_44(
    service: Annotated[QuerySetService, Depends(QuerySetService)],
    query_set_in: QuerySet,
) -> QuerySetOut:
    result, err = service.create(44, query_set_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.put("/{query_set_id}")
def update_query_44(
    service: Annotated[QuerySetService, Depends(QuerySetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    query_set_id: str,
    query_set_in: QuerySet,
) -> QuerySetOut:
    result, err = service.update(44, query_set_id, query_set_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.delete("/{query_set_id}")
def delete_query_set_44(
    service: Annotated[QuerySetService, Depends(QuerySetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    query_set_id: str,
) -> Mapping[str, str]:
    result, err = service.delete(44, query_set_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.get("/")
def list_query_set_223(
    service: Annotated[QuerySetService, Depends(QuerySetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin]))],
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[QuerySetOut]:
    result, err = service.get(44, page, limit)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.get("/{query_set_id}")
def get_one_query_set_223(
    service: Annotated[QuerySetService, Depends(QuerySetService)],
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    query_set_id: str,
) -> QuerySetOut:
    result, err = service.get_one(44, query_set_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.post("/")
def create_query_set_223(
    service: Annotated[QuerySetService, Depends(QuerySetService)],
    query_set_in: QuerySet,
) -> QuerySetOut:
    result, err = service.create(44, query_set_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.put("/{query_set_id}")
def update_query_set_223(
    service: Annotated[QuerySetService, Depends(QuerySetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    query_set_id: str,
    query_set_in: QuerySet,
) -> QuerySetOut:
    result, err = service.update(44, query_set_id, query_set_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.delete("/{query_set_id}")
def delete_query_set_223(
    service: Annotated[QuerySetService, Depends(QuerySetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    query_set_id: str,
) -> Mapping[str, str]:
    result, err = service.delete(44, query_set_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result
