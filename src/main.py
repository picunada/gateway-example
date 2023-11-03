from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import auth, field_set, generate, query_set, report, user

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
]

app = FastAPI(title="Multitender gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
router.include_router(generate.router, prefix="/generate", tags=["Generate"])

app.include_router(router, prefix="/api/v1")
app.include_router(router, prefix="/api/v1")
app.include_router(router, prefix="/api/v1")
