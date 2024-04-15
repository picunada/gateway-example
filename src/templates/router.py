from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.auth.dependencies import UserWithRole
from src.report.schemas import ReportOut
from src.report.service import ReportService
from src.schemas import PaginatedResponse
from src.user.schemas import Roles, UserInDb

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

