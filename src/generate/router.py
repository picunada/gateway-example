from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException

from src.auth.service import Auth
from src.generate.schemas import User, GenerateSettings, Schedule
from src.generate.service import GenerateService

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


@router.post("/stop")
def stop(
    key: str,
    service: Annotated[GenerateService, Depends(GenerateService)],
):
    result, err = service.stop_schedule(key)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result
