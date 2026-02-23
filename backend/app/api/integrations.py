from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.connectors.yandex_metrika import YandexMetrikaConnector
from app.connectors.yandex_direct import YandexDirectConnector
from app.connectors.vk_ads import VKAdsConnector
from app.db.session import get_db
from app.models.entities import MarketingDailyMetric, RawEvent, User

router = APIRouter(prefix="/integrations", tags=["integrations"])

CONNECTORS = {
    "yandex_metrika": YandexMetrikaConnector(),
    "yandex_direct": YandexDirectConnector(),
    "vk_ads": VKAdsConnector(),
}


@router.get("")
def list_integrations(_: User = Depends(get_current_user)):
    return {
        "items": [
            {"key": key, "title": key.replace("_", " ").title(), "mode": "demo", "status": "ready"}
            for key in CONNECTORS
        ]
    }


@router.post("/{connector_key}/sync")
def sync_connector(
    connector_key: str,
    date_from: date,
    date_to: date,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "marketer")),
):
    connector = CONNECTORS.get(connector_key)
    if connector is None:
        raise HTTPException(status_code=404, detail="Неизвестный коннектор")
    rows = connector.fetch(date_from, date_to)

    for item in rows:
        db.add(RawEvent(source=connector_key, payload=item, event_time=datetime.fromisoformat(item["metric_date"])))
        db.merge(MarketingDailyMetric(**item))

    db.commit()
    return {"synced_rows": len(rows), "connector": connector_key}
