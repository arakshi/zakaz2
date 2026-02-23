from datetime import date, timedelta

from app.connectors.yandex_direct import YandexDirectConnector
from app.connectors.yandex_metrika import YandexMetrikaConnector
from app.connectors.vk_ads import VKAdsConnector
from app.db.session import SessionLocal
from app.models.entities import MarketingDailyMetric
from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.jobs.daily_sync")
def daily_sync(days_back: int = 1):
    db = SessionLocal()
    try:
        date_to = date.today()
        date_from = date_to - timedelta(days=days_back)
        connectors = [YandexMetrikaConnector(), YandexDirectConnector(), VKAdsConnector()]
        for connector in connectors:
            for row in connector.fetch(date_from, date_to):
                db.merge(MarketingDailyMetric(**row))
        db.commit()
        return {"status": "ok"}
    finally:
        db.close()
