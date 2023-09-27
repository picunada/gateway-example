from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from src.auth.dependencies import UserWithRole
from src.auth.service import Auth
from src.schemas import PaginatedResponse
from src.user.schemas import Roles, User, UserIn, UserOut

from src.user.service import UserService

router = APIRouter()
auth = Auth()


@router.get("/", status_code=status.HTTP_200_OK)
async def list_users(
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    service: Annotated[UserService, Depends(UserService())],
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[UserOut]:
    result = service.list(page, limit)
    return result


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_one(
    user_id: str,
    service: Annotated[UserService, Depends(UserService())],
) -> UserOut:
    user = service.get_one(user_id)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def insert(
    user: Annotated[UserIn, Body(embed=False)],
    service: Annotated[UserService, Depends(UserService())],
) -> UserOut:
    created = service.insert_one(user)
    return created


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def put(
    user_id: str,
    user: Annotated[User, Body(embed=False)],
    service: Annotated[UserService, Depends(UserService())],
) -> UserOut:
    updated = service.update(user, user_id)
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    user_id: str, service: Annotated[UserService, Depends(UserService())]
) -> JSONResponse:
    deleted = service.delete(user_id)
    return deleted
