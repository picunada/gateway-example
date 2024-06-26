from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException

from src.auth.dependencies import UserWithRole
from src.auth.service import Auth
from src.generate.schemas import GenerateSettings, Schedule, User
from src.generate.service import GenerateService
from src.user.schemas import Roles, UserInDb

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


@router.websocket("/one/ws")
async def generate_one_ws(
    websocket: WebSocket,
    user: Annotated[UserInDb, Depends(WsUserWithRole([Roles.admin, Roles.default]))],
    service: Annotated[GenerateService, Depends(GenerateService)],
):
    rabbit = await get_rabbit_mq_client()
    await websocket.accept()

    while True:
        message = await websocket.receive_json()
        try:
            if message["message"] and message["message"] == "ping":
                await websocket.send_json({"message": "pong"})
        except KeyError:
            print("received not ping pong message")

        try:
            v_user = User.model_validate(user.model_dump())

            report_settings = GenerateSettings.model_validate(message)

            settings = {
                "user": v_user.model_dump(),
                "report_settings": report_settings.model_dump(),
            }

            result, err = service.generate_one(settings)

            print(result)

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

                print(queue_name)

                async with queue.iterator() as iter:
                    async for message in iter:
                        await websocket.send_json(message.body.decode())
                        break

            print("exit ws")

        except ValidationError as err:
            await websocket.send_json(err.json())
        
        rabbit.close()

        print("exit ws2")
        break

    print("closing ws")
    await websocket.close()


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
