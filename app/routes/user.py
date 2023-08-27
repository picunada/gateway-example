from typing import Optional, Annotated

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, status, Body
from starlette.responses import JSONResponse

from app.dependencies.auth import Auth, UserWithRole
from app.dependencies.db import MongoDatabase, get_database
from app.models.common import PaginatedResponse
from app.models.user import UserIn, Roles, User, UserOut, UserInDb

router = APIRouter()
auth = Auth()


@router.get("/", status_code=status.HTTP_200_OK)
async def list_users(
    user: Annotated[bool, Depends(UserWithRole([Roles.admin]))],
    db: Optional[MongoDatabase] = Depends(get_database),
    page: int = 1,
    limit: int = 15,
) -> PaginatedResponse[UserOut]:
    assert db is not None
    mongo = db.client
    users = mongo.get_database("mt-services")["users"]
    cursor = users.find().skip(limit * (page - 1)).limit(limit)
    serialized = list(map(lambda x: UserOut.model_validate(x), cursor))

    result = PaginatedResponse[UserOut](
        page=page,
        count=len(serialized),
        total=users.count_documents({}),
        results=serialized,
    )
    return result


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_one(
    id: str, db: Optional[MongoDatabase] = Depends(get_database)
) -> UserOut:
    assert db is not None
    mongo = db.client
    reports = mongo.get_database("mt-services")["users"]
    try:
        user = reports.find_one(ObjectId(id))
        if user is not None:
            return UserOut.model_validate(user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid ID should be 12-byt hex string",
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def insert(
    user: Annotated[UserIn, Body(embed=False)],
    db: Optional[MongoDatabase] = Depends(get_database),
) -> UserOut:
    assert db is not None
    mongo = db.client
    users = mongo.get_database("mt-services")["users"]
    hashed_password = auth.get_password_hash(user.password)
    user_in_db = UserInDb(
        **user.model_dump(), hashed_password=hashed_password, role=Roles.default
    )
    id = users.insert_one(user_in_db.model_dump()).inserted_id
    user_data = users.find_one(ObjectId(id))
    user_out = UserOut.model_validate(user_data)
    return user_out


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def put(
    id: str,
    user: Annotated[User, Body(embed=False)],
    db: Optional[MongoDatabase] = Depends(get_database),
) -> UserOut:
    assert db is not None
    mongo = db.client
    users = mongo.get_database("mt-services")["users"]
    try:
        found = users.find_one({"_id": ObjectId(id)})
        if found is not None:
            updated = users.update_one(
                {"_id": found["_id"]}, {"$set": user.model_dump()}
            )
            user_data = users.find_one(updated.upserted_id)
            user_out = UserOut.model_validate(user_data)
            return user_out
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid ID should be 12-byte hex string",
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: str, db: Optional[MongoDatabase] = Depends(get_database)
) -> JSONResponse:
    assert db is not None
    mongo = db.client
    users = mongo.get_database("mt-services")["users"]
    try:
        delete_result = users.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            return JSONResponse(
                content={"detail": "OK"}, status_code=status.HTTP_204_NO_CONTENT
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid ID should be 12-byte hex string",
        )
