from fastapi import FastAPI, APIRouter
from src import user, auth, report

app = FastAPI(title="Multitender gateway")
router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(report.router44, prefix="/report44", tags=["Report 44"])

app.include_router(router, prefix="/api/v1")
