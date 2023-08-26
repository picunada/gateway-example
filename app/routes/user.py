from typing import Optional, Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import ValidationError
from starlette.responses import JSONResponse

from app.dependencies.auth import Auth, UserWithRole
from app.dependencies.db import MongoDatabase, get_database
from app.models.common import PaginatedResponse
from app.models.user import UserIn, Roles, UserInDb

router = APIRouter()
auth = Auth()


@router.get("/", status_code=status.HTTP_200_OK)
async def list_users(
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    db: Optional[MongoDatabase] = Depends(get_database),
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[UserInDb]:
    assert db is not None
    mongo = db.client
    users = mongo.get_database("mt-services")["users"]
    cursor = users.find().skip(limit * (page - 1)).limit(limit)
    print(user)

    try:
        serialized = list(map(lambda x: UserInDb.model_validate(x), cursor))
    except ValidationError as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )
    result = PaginatedResponse[UserInDb](
        page=page,
        count=len(serialized),
        total=users.count_documents({}),
        results=serialized,
    )
    return result


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_one(
    id: str, db: Optional[MongoDatabase] = Depends(get_database)
) -> UserInDb:
    assert db is not None
    mongo = db.client
    reports = mongo.get_database("mt-services")["users"]
    user = reports.find_one(ObjectId(id))
    if user is not None:
        try:
            user = UserInDb.model_validate(user)
        except ValidationError as err:
            print(err)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            )
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def insert(
    user: Annotated[UserIn, Body(embed=False)],
    db: Optional[MongoDatabase] = Depends(get_database),
) -> UserInDb:
    assert db is not None
    mongo = db.client
    users = mongo.get_database("mt-services")["users"]
    hashed_password = auth.get_password_hash(user.password)
    user_in_db = UserInDb(
        **user.model_dump(), hashed_password=hashed_password, role=Roles.default
    )

    id = users.insert_one(user_in_db.model_dump()).inserted_id
    user_data = users.find_one(ObjectId(id))
    if user is not None:
        try:
            user_in_db = UserInDb.model_validate(user_data)
        except ValidationError as err:
            print(err)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            )
        return user_in_db

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not created")


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def put(
    id: str,
    user: Annotated[UserIn, Body(embed=False)],
    db: Optional[MongoDatabase] = Depends(get_database),
) -> UserInDb:
    assert db is not None
    mongo = db.client
    users = mongo.get_database("mt-services")["users"]
    updated = users.update_one({"_id": ObjectId(id)}, user.model_dump())
    user_data = users.find_one(updated.upserted_id)
    user_in_db = UserInDb.model_validate(user_data)
    return user_in_db


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: str, db: Optional[MongoDatabase] = Depends(get_database)
) -> JSONResponse:
    assert db is not None
    mongo = db.client
    users = mongo.get_database("mt-services")["users"]
    delete_result = users.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(
            content={"status": "OK"}, status_code=status.HTTP_204_NO_CONTENT
        )

    raise HTTPException(status_code=404, detail=f"User {id} not found")
