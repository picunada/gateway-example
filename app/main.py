from fastapi import FastAPI, APIRouter
from app.routes import user, auth

app = FastAPI()
router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])

app.include_router(router, prefix="/api/v1")
