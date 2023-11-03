from typing import Annotated, Mapping

from fastapi import APIRouter, Depends, HTTPException

from src.auth.dependencies import UserWithRole
from src.schemas import PaginatedResponse
from src.report.schemas import ReportOut, ReportIn
from src.user.schemas import Roles, UserInDb
from src.report.service import ReportService

router44 = APIRouter()
router223 = APIRouter()


@router44.get("/")
def list_reports_44(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin, Roles.default]))],
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[ReportOut]:
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


@router44.get("/{report_id}")
def get_one_report_44(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    report_id: str,
) -> ReportOut:
    result, err = service.get_one(44, report_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.post("/")
def create_report_44(
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin, Roles.default]))],
    service: Annotated[ReportService, Depends(ReportService)],
    report_in: ReportIn,
) -> ReportOut:
    result, err = service.create(str(user.id), 44, report_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.put("/{report_id}")
def update_report_44(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    report_id: str,
    report_in: ReportIn,
) -> ReportOut:
    result, err = service.update(44, report_id, report_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router44.delete("/{report_id}")
def delete_report_44(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    report_id: str,
) -> Mapping[str, str]:
    result, err = service.delete(44, report_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.get("/")
def list_reports_223(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin, Roles.default]))],
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[ReportOut]:
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


@router223.get("/{report_id}")
def get_one_report_223(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    report_id: str,
) -> ReportOut:
    result, err = service.get_one(223, report_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.post("/")
def create_report_223(
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.admin, Roles.default]))],
    service: Annotated[ReportService, Depends(ReportService)],
    report_in: ReportIn,
) -> ReportOut:
    print(report_in.model_dump(by_alias=True))
    result, err = service.create(str(user.id), 223, report_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.put("/{report_id}")
def update_report_223(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    report_id: str,
    report_in: ReportIn,
) -> ReportOut:
    result, err = service.update(44, report_id, report_in)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router223.delete("/{report_id}")
def delete_report_223(
    service: Annotated[ReportService, Depends(ReportService)],
    user: Annotated[UserInDb, Depends(UserWithRole([]))],
    report_id: str,
) -> Mapping[str, str]:
    result, err = service.delete(44, report_id)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result
