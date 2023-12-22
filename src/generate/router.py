import json
import os
from typing import Annotated
from dotenv import load_dotenv

from fastapi import APIRouter, Body, Depends, HTTPException, WebSocket
from pydantic_core._pydantic_core import ValidationError

from src.auth.dependencies import UserWithRole, WsUserWithRole
from src.auth.service import Auth
from src.generate.schemas import User, GenerateSettings, Schedule
from src.generate.service import GenerateService
from src.rabbit_mq import get_rabbit_mq_client
from src.user.schemas import UserInDb, Roles

load_dotenv()

router = APIRouter()

auth = Auth()


@router.post("/one")
def generate_one(
    user: Annotated[User, Body(embed=True)],
    report_settings: Annotated[GenerateSettings, Body(embed=True)],
    service: Annotated[GenerateService, Depends(GenerateService)],
):
    v_user = User.model_validate(user)

    settings = {
        "user": v_user.model_dump(),
        "report_settings": report_settings.model_dump(),
    }
    result, err = service.generate_one(settings)

    if err:
        status_code, detail = err
        raise HTTPException(status_code, detail)

    assert result is not None

    return result


@router.websocket("/one/ws")
async def generate_one_ws(
    websocket: WebSocket,
    user: Annotated[UserInDb, Depends(WsUserWithRole([Roles.admin, Roles.default]))],
    service: Annotated[GenerateService, Depends(GenerateService)],
):
    await websocket.accept()

    rabbit = await get_rabbit_mq_client()

    while True:
        data = json.loads(await websocket.receive_text())

        try:
            v_user = User.model_validate(user.model_dump())

            report_settings = GenerateSettings.model_validate(data)

            settings = {
                "user": v_user.model_dump(),
                "report_settings": report_settings.model_dump(),
            }

            await websocket.send_json(settings)

            result, err = service.generate_one(settings)

            if err:
                status_code, detail = err
                raise HTTPException(status_code, detail)

            assert result is not None

            async with rabbit:
                channel = await rabbit.channel()

                queue_name = os.getenv("RABBIT_MQ_QUEUE")
                assert queue_name is not None
                # Declaring queue
                queue = await channel.declare_queue(
                    queue_name + f"-{user.username}", auto_delete=True
                )

                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            print(message.body.decode())

                            await websocket.send_json(message.body.decode())
                            await websocket.close()

                            break

        except ValidationError as err:
            await websocket.send_json(err.json())


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
