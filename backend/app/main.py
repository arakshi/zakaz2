from fastapi import FastAPI

from app.api import auth, analytics, integrations, reports, data
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(analytics.router, prefix=settings.api_v1_prefix)
app.include_router(integrations.router, prefix=settings.api_v1_prefix)
app.include_router(reports.router, prefix=settings.api_v1_prefix)
app.include_router(data.router, prefix=settings.api_v1_prefix)


@app.get("/")
def healthcheck():
    return {"status": "ok", "app": settings.app_name}
