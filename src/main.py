from fastapi import FastAPI, APIRouter
from src import user, auth, report

app = FastAPI(title="Multitender gateway")
router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(report.router44, prefix="/report/44", tags=["Report 44"])
router.include_router(report.router223, prefix="/report/223", tags=["Report 223"])

app.include_router(router, prefix="/api/v1")
