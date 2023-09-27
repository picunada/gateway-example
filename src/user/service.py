import os
from typing import Optional
from fastapi import Depends, HTTPException, status
from starlette.responses import JSONResponse

from src.auth.service import Auth
from src.database import MongoDatabase, get_database
from src.schemas import PaginatedResponse
from src.user.schemas import UserOut, UserIn, UserInDb, Roles, User
from bson import ObjectId
from bson.errors import InvalidId


class UserService:
    def __init__(self):
        self.auth = Auth()

    def __call__(self, db: Optional[MongoDatabase] = Depends(get_database)):
        assert db is not None
        self.db = db
        return self

    def list(self, page: int, limit: int):
        mongo = self.db.client
        users = mongo.get_database("mt-services")[f"users:{os.getenv('UVICORN_ENV')}"]
        cursor = users.find().skip(limit * (page - 1)).limit(limit)
        serialized = list(map(UserOut.model_validate, cursor))

        result = PaginatedResponse[UserOut](
            page=page,
            count=len(serialized),
            total=users.count_documents({}),
            results=serialized,
        )
        return result

    def get_one(self, user_id: str):
        mongo = self.db.client
        reports = mongo.get_database("mt-services")[f"users:{os.getenv('UVICORN_ENV')}"]
        try:
            user = reports.find_one(ObjectId(user_id))
            if user is not None:
                return UserOut.model_validate(user)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        except InvalidId as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid ID should be 12-byte hex string",
            ) from exc

    def insert_one(self, user: UserIn):
        mongo = self.db.client
        users = mongo.get_database("mt-services")[f"users:{os.getenv('UVICORN_ENV')}"]
        hashed_password = self.auth.get_password_hash(user.password)
        user_in_db = UserInDb(
            **user.model_dump(), hashed_password=hashed_password, role=Roles.default
        )
        user_id = users.insert_one(user_in_db.model_dump()).inserted_id
        user_data = users.find_one(ObjectId(user_id))
        user_out = UserOut.model_validate(user_data)
        return user_out

    def update(self, user: User, user_id: str):
        mongo = self.db.client
        users = mongo.get_database("mt-services")[f"users:{os.getenv('UVICORN_ENV')}"]
        try:
            found = users.find_one({"_id": ObjectId(user_id)})
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
        except InvalidId as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid ID should be 12-byte hex string",
            ) from exc

    def delete(self, user_id: str):
        mongo = self.db.client
        users = mongo.get_database("mt-services")[f"users:{os.getenv('UVICORN_ENV')}"]
        try:
            delete_result = users.delete_one({"_id": ObjectId(user_id)})
            if delete_result.deleted_count == 1:
                return JSONResponse(
                    content={"detail": "OK"}, status_code=status.HTTP_204_NO_CONTENT
                )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        except InvalidId as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid ID should be 12-byte hex string",
            ) from exc
