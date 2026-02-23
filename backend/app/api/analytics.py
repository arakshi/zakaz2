from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import MarketingDailyMetric, User
from app.services.insights import compare_periods, detect_anomalies, forecast_dates, forecast_linear, recommend_budget
from app.services.metrics import MetricRow, aggregate_metrics

router = APIRouter(prefix="/analytics", tags=["analytics"])
ALLOWED_FORECAST_METRICS = {"revenue", "orders", "visits", "cost"}


def _rows(db: Session, date_from: date, date_to: date):
    return db.query(MarketingDailyMetric).filter(
        and_(MarketingDailyMetric.metric_date >= date_from, MarketingDailyMetric.metric_date <= date_to)
    ).all()


@router.get("/overview")
def overview(date_from: date, date_to: date, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    current_rows = [MetricRow(r.visits, r.orders, r.revenue, r.cost, r.users_new, r.users_returning) for r in _rows(db, date_from, date_to)]
    current = aggregate_metrics(current_rows)

    days = (date_to - date_from).days + 1
    prev_from = date_from - timedelta(days=days)
    prev_to = date_from - timedelta(days=1)
    previous_rows = [MetricRow(r.visits, r.orders, r.revenue, r.cost, r.users_new, r.users_returning) for r in _rows(db, prev_from, prev_to)]
    previous = aggregate_metrics(previous_rows)

    return {"current": current, "previous": previous, "comments": compare_periods(current, previous)}


@router.get("/channels")
def channels(
    date_from: date,
    date_to: date,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    base = db.query(
        MarketingDailyMetric.channel,
        func.sum(MarketingDailyMetric.visits).label("visits"),
        func.sum(MarketingDailyMetric.orders).label("orders"),
        func.sum(MarketingDailyMetric.revenue).label("revenue"),
        func.sum(MarketingDailyMetric.cost).label("cost"),
    ).filter(and_(MarketingDailyMetric.metric_date >= date_from, MarketingDailyMetric.metric_date <= date_to)).group_by(MarketingDailyMetric.channel)

    grouped = base.offset((page - 1) * page_size).limit(page_size).all()
    items = []
    for row in grouped:
        conversion = (row.orders / row.visits) if row.visits else 0
        romi = ((row.revenue - row.cost) / row.cost) if row.cost else 0
        items.append({
            "channel": row.channel,
            "visits": int(row.visits or 0),
            "orders": int(row.orders or 0),
            "revenue": float(row.revenue or 0),
            "cost": float(row.cost or 0),
            "conversion": round(conversion, 4),
            "romi": round(romi, 4),
        })

    return {"items": items, "recommendations": recommend_budget(items), "page": page, "page_size": page_size}


@router.get("/forecast")
def forecast(metric: str, horizon: int = Query(30, ge=7, le=90), db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if metric not in ALLOWED_FORECAST_METRICS:
        raise HTTPException(status_code=400, detail=f"metric must be one of {sorted(ALLOWED_FORECAST_METRICS)}")

    today = date.today()
    from_day = today - timedelta(days=90)
    rows = db.query(MarketingDailyMetric.metric_date, func.sum(getattr(MarketingDailyMetric, metric))).filter(
        and_(MarketingDailyMetric.metric_date >= from_day, MarketingDailyMetric.metric_date <= today)
    ).group_by(MarketingDailyMetric.metric_date).order_by(MarketingDailyMetric.metric_date).all()

    history_values = [float(v or 0) for _, v in rows]
    forecast_values = forecast_linear(history_values, horizon)

    return {
        "metric": metric,
        "history": [{"date": d.isoformat(), "value": float(v or 0)} for d, v in rows],
        "anomaly_indices": detect_anomalies(history_values),
        "forecast": [{"date": d, "value": v} for d, v in zip(forecast_dates(today, horizon), forecast_values)],
    }
