from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analytics, auth, data, integrations, reports
from app.bootstrap import bootstrap_data, ensure_schema
from app.core.config import settings
from app.db.session import SessionLocal

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(analytics.router, prefix=settings.api_v1_prefix)
app.include_router(integrations.router, prefix=settings.api_v1_prefix)
app.include_router(data.router, prefix=settings.api_v1_prefix)
app.include_router(reports.router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
def startup_init() -> None:
    ensure_schema()
    db = SessionLocal()
    try:
        bootstrap_data(db)
    finally:
        db.close()


@app.get("/")
def health():
    return {"status": "ok", "app": settings.app_name}
