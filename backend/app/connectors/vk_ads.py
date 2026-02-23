from datetime import date, timedelta
from random import randint, uniform

from app.connectors.base import BaseConnector


class VKAdsConnector(BaseConnector):
    key = "vk_ads"
    title = "VK Реклама"

    def fetch(self, date_from: date, date_to: date) -> list[dict]:
        rows = []
        day = date_from
        while day <= date_to:
            visits = randint(200, 850)
            orders = int(visits * uniform(0.025, 0.07))
            rows.append(
                {
                    "metric_date": day,
                    "channel": self.title,
                    "campaign": "Ретаргетинг",
                    "device": "all",
                    "region": "all",
                    "visits": visits,
                    "orders": orders,
                    "revenue": round(orders * 3500, 2),
                    "cost": round(uniform(3000, 10000), 2),
                    "users_new": int(visits * 0.4),
                    "users_returning": int(visits * 0.15),
                }
            )
            day += timedelta(days=1)
        return rows
