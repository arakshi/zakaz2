from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import GeneratedReport, ReportTemplate, User

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/templates")
def create_template(name: str, config: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    template = ReportTemplate(name=name, config=config, created_by=user.id)
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


@router.post("/generate")
def generate_report(template_id: int, period_from: date, period_to: date, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    template = db.query(ReportTemplate).get(template_id)
    html = f"<html><body><h1>Отчет {template.name}</h1><p>Период: {period_from} — {period_to}</p></body></html>"
    report = GeneratedReport(template_id=template_id, period_from=period_from, period_to=period_to, html_content=html)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.get("")
def list_reports(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    reports = db.query(GeneratedReport).order_by(GeneratedReport.created_at.desc()).all()
    return {"items": reports}
