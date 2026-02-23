from datetime import date, timedelta
from random import randint, uniform

from app.connectors.base import BaseConnector


class YandexDirectConnector(BaseConnector):
    key = "yandex_direct"
    title = "Яндекс Директ"

    def fetch(self, date_from: date, date_to: date) -> list[dict]:
        rows = []
        day = date_from
        while day <= date_to:
            visits = randint(300, 1100)
            orders = int(visits * uniform(0.03, 0.08))
            rows.append(
                {
                    "metric_date": day,
                    "channel": self.title,
                    "campaign": "Поиск-Бренд",
                    "device": "all",
                    "region": "all",
                    "visits": visits,
                    "orders": orders,
                    "revenue": round(orders * 4100, 2),
                    "cost": round(uniform(4000, 13000), 2),
                    "users_new": int(visits * 0.38),
                    "users_returning": int(visits * 0.22),
                }
            )
            day += timedelta(days=1)
        return rows
