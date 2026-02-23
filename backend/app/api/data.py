from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.connectors.universal import parse_uploaded_file
from app.db.session import get_db
from app.models.entities import MarketingDailyMetric, RawEvent, User

router = APIRouter(prefix="/data", tags=["data"])
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    destination = UPLOAD_DIR / file.filename
    destination.write_bytes(await file.read())

    try:
        rows = parse_uploaded_file(str(destination))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    imported = 0
    for row in rows:
        db.add(RawEvent(source="manual_upload", payload=row, event_time=datetime.fromisoformat(str(row["metric_date"]))))
        db.merge(MarketingDailyMetric(**row))
        imported += 1
    db.commit()

    return {"imported": imported, "filename": file.filename}
