from datetime import date, timedelta
import random

from app.connectors.base import Connector, DemoMixin


class VKAdsConnector(DemoMixin, Connector):
    name = "vk_ads"

    def fetch(self, date_from: date, date_to: date) -> list[dict]:
        records = []
        day = date_from
        while day <= date_to:
            visits = random.randint(250, 800)
            orders = int(visits * random.uniform(0.025, 0.07))
            records.append(self._fake_row(day.isoformat(), "VK Реклама", "Ретаргетинг", random.uniform(4000, 11000), visits, orders))
            day += timedelta(days=1)
        return records
