from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.connectors.universal import parse_uploaded_file
from app.db.session import get_db
from app.models.entities import MarketingDailyMetric, RawEvent, User

router = APIRouter(prefix="/data", tags=["data"])

UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_data(file: UploadFile = File(...), db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    file_path = UPLOAD_DIR / file.filename
    file_path.write_bytes(await file.read())

    try:
        rows = parse_uploaded_file(str(file_path))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    imported = 0
    for item in rows:
        db.add(RawEvent(source="manual_upload", payload=item, event_time=datetime.fromisoformat(str(item["metric_date"]))))
        db.merge(MarketingDailyMetric(**item))
        imported += 1

    db.commit()
    return {"imported": imported, "filename": file.filename}
