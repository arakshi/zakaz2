from datetime import date, timedelta
import random

from app.connectors.base import Connector, DemoMixin


class YandexMetrikaConnector(DemoMixin, Connector):
    name = "yandex_metrika"

    def fetch(self, date_from: date, date_to: date) -> list[dict]:
        records = []
        day = date_from
        while day <= date_to:
            visits = random.randint(300, 900)
            orders = int(visits * random.uniform(0.02, 0.06))
            records.append(self._fake_row(day.isoformat(), "Яндекс.Метрика", "Органика", random.uniform(1500, 6500), visits, orders))
            day += timedelta(days=1)
        return records
