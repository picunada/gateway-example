from fastapi import FastAPI, APIRouter
from app.routes import user, auth, report44

app = FastAPI()
router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(report44.router, prefix="/report44", tags=["Report 44"])

app.include_router(router, prefix="/api/v1")
