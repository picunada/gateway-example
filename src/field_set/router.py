from typing import Annotated, Mapping

from fastapi import APIRouter, Depends, HTTPException

from src.auth.dependencies import UserWithRole
from src.field_set.schemas import FieldSet, FieldSetOut
from src.field_set.service import FieldSetService
from src.schemas import PaginatedResponse
from src.user.schemas import Roles, UserInDb

router44 = APIRouter()
router223 = APIRouter()


@router44.get("/")
def list_fields_set_44(
    service: Annotated[FieldSetService, Depends(FieldSetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin]))],
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[FieldSetOut]:
    result, err = service.get(44, page, limit)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.get("/{field_set_id}")
def get_one_field_set_44(
    service: Annotated[FieldSetService, Depends(FieldSetService)],
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    field_set_id: str,
) -> FieldSetOut:
    result, err = service.get_one(44, field_set_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.post("/")
def create_field_set_44(
    service: Annotated[FieldSetService, Depends(FieldSetService)],
    field_set_in: FieldSet,
) -> FieldSetOut:
    result, err = service.create(44, field_set_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.put("/{field_set_id}")
def update_query_44(
    service: Annotated[FieldSetService, Depends(FieldSetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    field_set_id: str,
    field_set_in: FieldSet,
) -> FieldSetOut:
    result, err = service.update(44, field_set_id, field_set_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.delete("/{field_set_id}")
def delete_field_set_44(
    service: Annotated[FieldSetService, Depends(FieldSetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    field_set_id: str,
) -> Mapping[str, str]:
    result, err = service.delete(44, field_set_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.get("/")
def list_field_set_223(
    service: Annotated[FieldSetService, Depends(FieldSetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin]))],
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[FieldSetOut]:
    result, err = service.get(223, page, limit)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.get("/{field_set_id}")
def get_one_field_set_223(
    service: Annotated[FieldSetService, Depends(FieldSetService)],
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    field_set_id: str,
) -> FieldSetOut:
    result, err = service.get_one(223, field_set_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.post("/")
def create_field_set_223(
    service: Annotated[FieldSetService, Depends(FieldSetService)],
    field_set_in: FieldSet,
) -> FieldSetOut:
    result, err = service.create(223, field_set_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.put("/{field_set_id}")
def update_field_set_223(
    service: Annotated[FieldSetService, Depends(FieldSetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    field_set_id: str,
    field_set_in: FieldSet,
) -> FieldSetOut:
    result, err = service.update(223, field_set_id, field_set_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.delete("/{field_set_id}")
def delete_field_set_223(
    service: Annotated[FieldSetService, Depends(FieldSetService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    field_set_id: str,
) -> Mapping[str, str]:
    result, err = service.delete(223, field_set_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result
