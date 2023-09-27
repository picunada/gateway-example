from fastapi import FastAPI, APIRouter
from src import user, auth, report, field_set, query_set

app = FastAPI(title="Multitender gateway")
router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(report.router44, prefix="/report/44", tags=["Report 44"])
router.include_router(report.router223, prefix="/report/223", tags=["Report 223"])
router.include_router(field_set.router44, prefix="/field_set/44", tags=["FieldSet 44"])
router.include_router(
    field_set.router223, prefix="/field_set/223", tags=["FieldSet 223"]
)
router.include_router(query_set.router44, prefix="/query_set/44", tags=["QuerySet 44"])
router.include_router(
    query_set.router223, prefix="/query_set/223", tags=["QuerySet 223"]
)

app.include_router(router, prefix="/api/v1")
