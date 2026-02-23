from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import GeneratedReport, ReportTemplate, User

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/templates")
def create_template(name: str, config: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exists = db.query(ReportTemplate).filter(ReportTemplate.name == name).first()
    if exists:
        raise HTTPException(status_code=409, detail="Шаблон уже существует")
    template = ReportTemplate(name=name, config=config, created_by=user.id)
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


@router.post("/generate")
def generate(template_id: int, period_from: date, period_to: date, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    template = db.query(ReportTemplate).filter(ReportTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Шаблон не найден")

    html = f"<html><body><h1>{template.name}</h1><p>Период: {period_from} - {period_to}</p></body></html>"
    report = GeneratedReport(template_id=template.id, period_from=period_from, period_to=period_to, html_content=html)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.get("")
def list_reports(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    items = db.query(GeneratedReport).order_by(GeneratedReport.created_at.desc()).all()
    return {"items": items}
