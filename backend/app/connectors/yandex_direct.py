from datetime import date, timedelta
import random

from app.connectors.base import Connector, DemoMixin


class YandexDirectConnector(DemoMixin, Connector):
    name = "yandex_direct"

    def fetch(self, date_from: date, date_to: date) -> list[dict]:
        records = []
        day = date_from
        while day <= date_to:
            visits = random.randint(200, 700)
            orders = int(visits * random.uniform(0.03, 0.09))
            records.append(self._fake_row(day.isoformat(), "Яндекс.Директ", "Поиск-Бренд", random.uniform(6000, 15000), visits, orders))
            day += timedelta(days=1)
        return records
