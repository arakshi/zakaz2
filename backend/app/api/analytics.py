from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import MarketingDailyMetric, User
from app.services.metrics import MetricRow, aggregate_metrics
from app.services.insights import budget_recommendations, compare_periods, detect_anomalies, forecast_linear, build_forecast_dates

router = APIRouter(prefix="/analytics", tags=["analytics"])

ALLOWED_FORECAST_METRICS = {"revenue", "orders", "visits", "cost"}


def _query_rows(db: Session, date_from: date, date_to: date):
    return (
        db.query(MarketingDailyMetric)
        .filter(and_(MarketingDailyMetric.metric_date >= date_from, MarketingDailyMetric.metric_date <= date_to))
        .all()
    )


@router.get("/overview")
def overview(date_from: date, date_to: date, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = _query_rows(db, date_from, date_to)
    metric_rows = [MetricRow(**{k: getattr(r, k) for k in MetricRow.__annotations__.keys()}) for r in rows]
    current = aggregate_metrics(metric_rows)

    period_days = (date_to - date_from).days + 1
    previous_from = date_from - timedelta(days=period_days)
    previous_to = date_from - timedelta(days=1)

    prev_rows = _query_rows(db, previous_from, previous_to)
    prev_metric_rows = [MetricRow(**{k: getattr(r, k) for k in MetricRow.__annotations__.keys()}) for r in prev_rows]
    previous = aggregate_metrics(prev_metric_rows)

    return {
        "current": current,
        "previous": previous,
        "comments": compare_periods(current, previous),
    }


@router.get("/channels")
def channels(date_from: date, date_to: date, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    grouped = (
        db.query(
            MarketingDailyMetric.channel,
            func.sum(MarketingDailyMetric.visits),
            func.sum(MarketingDailyMetric.orders),
            func.sum(MarketingDailyMetric.revenue),
            func.sum(MarketingDailyMetric.cost),
        )
        .filter(and_(MarketingDailyMetric.metric_date >= date_from, MarketingDailyMetric.metric_date <= date_to))
        .group_by(MarketingDailyMetric.channel)
        .all()
    )

    data = []
    for channel, visits, orders, revenue, cost in grouped:
        conversion = (orders / visits) if visits else 0
        romi = ((revenue - cost) / cost) if cost else 0
        data.append({
            "channel": channel,
            "visits": int(visits or 0),
            "orders": int(orders or 0),
            "revenue": float(revenue or 0),
            "cost": float(cost or 0),
            "conversion": round(conversion, 4),
            "romi": round(romi, 4),
        })

    return {"channels": data, "recommendations": budget_recommendations(data)}


@router.get("/forecast")
def forecast(metric: str, horizon: int = 30, date_from: date | None = None, date_to: date | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if metric not in ALLOWED_FORECAST_METRICS:
        raise HTTPException(status_code=400, detail=f"Недопустимая метрика. Доступно: {sorted(ALLOWED_FORECAST_METRICS)}")
    date_to = date_to or date.today()
    date_from = date_from or (date_to - timedelta(days=90))

    rows = (
        db.query(MarketingDailyMetric.metric_date, func.sum(getattr(MarketingDailyMetric, metric)))
        .filter(and_(MarketingDailyMetric.metric_date >= date_from, MarketingDailyMetric.metric_date <= date_to))
        .group_by(MarketingDailyMetric.metric_date)
        .order_by(MarketingDailyMetric.metric_date)
        .all()
    )

    history = [float(v or 0) for _, v in rows]
    anomalies = detect_anomalies(history)
    forecast_values = forecast_linear(history, horizon)
    return {
        "metric": metric,
        "history": [{"date": d.isoformat(), "value": float(v)} for d, v in rows],
        "anomaly_indices": anomalies,
        "forecast": [
            {"date": day, "value": value}
            for day, value in zip(build_forecast_dates(date_to, horizon), forecast_values)
        ],
    }
