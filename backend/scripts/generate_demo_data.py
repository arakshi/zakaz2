from datetime import date, timedelta
from random import choice, randint, uniform

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.entities import MarketingDailyMetric, User


def seed_users(db):
    users = [
        ("admin@fup.ru", "Администратор", "admin", "admin123"),
        ("marketer@fup.ru", "Маркетолог", "marketer", "marketer123"),
        ("analyst@fup.ru", "Аналитик", "analyst", "analyst123"),
    ]
    for email, full_name, role, password in users:
        if not db.query(User).filter(User.email == email).first():
            db.add(User(email=email, full_name=full_name, role=role, hashed_password=get_password_hash(password)))


def seed_metrics(db, days: int = 180):
    channels = {
        "Яндекс Директ": ["Поиск-Бренд", "РСЯ-Ремаркетинг"],
        "VK Реклама": ["Ретаргетинг", "Лидогенерация"],
        "Яндекс Метрика": ["Органика"],
    }

    today = date.today()
    for i in range(days):
        metric_date = today - timedelta(days=i)
        for channel, campaigns in channels.items():
            for campaign in campaigns:
                visits = randint(120, 1400)
                orders = int(visits * uniform(0.02, 0.09))
                revenue = round(orders * uniform(2500, 6000), 2)
                cost = round(visits * uniform(8, 28), 2)
                db.merge(
                    MarketingDailyMetric(
                        metric_date=metric_date,
                        channel=channel,
                        campaign=campaign,
                        device=choice(["desktop", "mobile"]),
                        region=choice(["Москва", "СПб", "Казань", "Новосибирск"]),
                        visits=visits,
                        orders=orders,
                        revenue=revenue,
                        cost=cost,
                        users_new=int(visits * uniform(0.22, 0.5)),
                        users_returning=int(visits * uniform(0.1, 0.28)),
                    )
                )


def run():
    db = SessionLocal()
    try:
        seed_users(db)
        seed_metrics(db)
        db.commit()
        print("Demo data seeded successfully")
    finally:
        db.close()


if __name__ == "__main__":
    run()
