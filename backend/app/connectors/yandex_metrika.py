from datetime import date, timedelta
from random import randint, uniform

from app.connectors.base import BaseConnector


class YandexMetrikaConnector(BaseConnector):
    key = "yandex_metrika"
    title = "Яндекс Метрика"

    def fetch(self, date_from: date, date_to: date) -> list[dict]:
        rows = []
        day = date_from
        while day <= date_to:
            visits = randint(200, 900)
            orders = int(visits * uniform(0.02, 0.05))
            rows.append(
                {
                    "metric_date": day,
                    "channel": self.title,
                    "campaign": "Органика",
                    "device": "all",
                    "region": "all",
                    "visits": visits,
                    "orders": orders,
                    "revenue": round(orders * 3200, 2),
                    "cost": round(uniform(1000, 5000), 2),
                    "users_new": int(visits * 0.35),
                    "users_returning": int(visits * 0.2),
                }
            )
            day += timedelta(days=1)
        return rows
