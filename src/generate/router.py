from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException

from src.auth.dependencies import UserWithRole
from src.auth.service import Auth
from src.generate.schemas import User, GenerateSettings, Schedule
from src.generate.service import GenerateService
from src.user.schemas import UserInDb, Roles

router = APIRouter()

auth = Auth()


@router.post("/one")
def generate_one(
    user: Annotated[User, Body(embed=True)],
    report_settings: Annotated[GenerateSettings, Body(embed=True)],
    service: Annotated[GenerateService, Depends(GenerateService)],
):
    settings = {
        "user": user.model_dump(),
        "report_settings": report_settings.model_dump(),
    }
    result, err = service.generate_one(settings)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router.post("/schedule")
def generate_schedule(
    user: Annotated[User, Body(embed=True)],
    cron: Annotated[Schedule, Body(embed=True)],
    report_settings: Annotated[GenerateSettings, Body(embed=True)],
    service: Annotated[GenerateService, Depends(GenerateService)],
):
    settings = {
        "user": user.model_dump(),
        "cron": cron.model_dump(),
        "report_settings": report_settings.model_dump(),
    }
    result, err = service.generate_scheduled(settings)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router.post("/stop/{subcription_id}")
def stop(
    subcription_id: str,
    user: Annotated[UserInDb, Depends(UserWithRole([Roles.default, Roles.admin]))],
    service: Annotated[GenerateService, Depends(GenerateService)],
):
    result, err = service.stop_schedule(subcription_id, user.id.__str__())

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result
