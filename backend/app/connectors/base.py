from abc import ABC, abstractmethod
from datetime import date


class Connector(ABC):
    name: str

    @abstractmethod
    def fetch(self, date_from: date, date_to: date) -> list[dict]:
        """Fetch marketing records for date range."""


class DemoMixin:
    def _fake_row(self, day: str, channel: str, campaign: str, cost: float, visits: int, orders: int) -> dict:
        return {
            "metric_date": day,
            "channel": channel,
            "campaign": campaign,
            "device": "desktop",
            "region": "Москва",
            "visits": visits,
            "orders": orders,
            "revenue": round(orders * 3200.0, 2),
            "cost": round(cost, 2),
            "users_new": int(visits * 0.3),
            "users_returning": int(visits * 0.2),
        }
