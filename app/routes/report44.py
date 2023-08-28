from typing import Annotated, Mapping

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import UserWithRole
from app.models.common import PaginatedResponse
from app.models.report import ReportOut, ReportIn
from app.models.user import Roles, UserInDb
from app.service.report import ReportService

router = APIRouter()


@router.get("/")
def list_reports(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin]))],
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[ReportOut]:
    result, err = service.get(44, page, limit)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router.get("/{id}")
def get_one(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    id: str,
) -> ReportOut:
    result, err = service.get_one(44, id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router.post("/")
def create(
    service: Annotated[ReportService, Depends(ReportService)], report_in: ReportIn
) -> ReportOut:
    result, err = service.create(44, report_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router.put("/{id}")
def update(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    id: str,
    report_in: ReportIn,
) -> ReportOut:
    result, err = service.update(44, id, report_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router.delete("/{id}")
def delete(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    id: str,
) -> Mapping[str, str]:
    result, err = service.delete(44, id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result
