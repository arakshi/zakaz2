from datetime import date, timedelta
import random

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.entities import MarketingDailyMetric, User


def run(days: int = 180):
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@fup.ru").first():
            db.add(User(email="admin@fup.ru", full_name="Администратор", hashed_password=get_password_hash("admin123"), role="admin"))

        channels = ["Яндекс.Директ", "VK Реклама", "Яндекс.Метрика"]
        campaigns = {
            "Яндекс.Директ": ["Поиск-Бренд", "РСЯ-Ремаркетинг"],
            "VK Реклама": ["Лидогенерация", "Ретаргетинг"],
            "Яндекс.Метрика": ["Органика"],
        }

        today = date.today()
        for i in range(days):
            day = today - timedelta(days=i)
            for channel in channels:
                for campaign in campaigns[channel]:
                    visits = random.randint(150, 1000)
                    orders = int(visits * random.uniform(0.02, 0.08))
                    revenue = round(orders * random.uniform(2400, 5600), 2)
                    cost = round(visits * random.uniform(9, 35), 2)

                    db.merge(
                        MarketingDailyMetric(
                            metric_date=day,
                            channel=channel,
                            campaign=campaign,
                            device=random.choice(["desktop", "mobile"]),
                            region=random.choice(["Москва", "Санкт-Петербург", "Казань", "Екатеринбург"]),
                            visits=visits,
                            orders=orders,
                            revenue=revenue,
                            cost=cost,
                            users_new=int(visits * random.uniform(0.2, 0.5)),
                            users_returning=int(visits * random.uniform(0.1, 0.3)),
                        )
                    )
        db.commit()
        print("Demo data generated")
    finally:
        db.close()


if __name__ == "__main__":
    run()
