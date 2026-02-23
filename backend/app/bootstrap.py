from datetime import date, timedelta
from random import choice, randint, uniform

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import Base, engine
from app.models.entities import MarketingDailyMetric, User


def ensure_schema() -> None:
    Base.metadata.create_all(bind=engine)


def ensure_default_users(db: Session) -> None:
    users = [
        ("admin@fup.ru", "Администратор", "admin", "admin123"),
        ("marketer@fup.ru", "Маркетолог", "marketer", "marketer123"),
        ("analyst@fup.ru", "Аналитик", "analyst", "analyst123"),
    ]
    for email, full_name, role, password in users:
        if not db.query(User).filter(User.email == email).first():
            db.add(User(email=email, full_name=full_name, role=role, hashed_password=get_password_hash(password)))


def ensure_demo_metrics(db: Session, days: int = 60) -> None:
    if db.query(MarketingDailyMetric).first():
        return

    channels = {
        "Яндекс Директ": ["Поиск-Бренд", "РСЯ-Ремаркетинг"],
        "VK Реклама": ["Ретаргетинг", "Лидогенерация"],
        "Яндекс Метрика": ["Органика"],
    }
    today = date.today()
    for i in range(days):
        day = today - timedelta(days=i)
        for channel, campaigns in channels.items():
            for campaign in campaigns:
                visits = randint(120, 1000)
                orders = int(visits * uniform(0.02, 0.08))
                db.add(
                    MarketingDailyMetric(
                        metric_date=day,
                        channel=channel,
                        campaign=campaign,
                        device=choice(["desktop", "mobile"]),
                        region=choice(["Москва", "СПб", "Казань"]),
                        visits=visits,
                        orders=orders,
                        revenue=round(orders * uniform(2500, 5500), 2),
                        cost=round(visits * uniform(8, 22), 2),
                        users_new=int(visits * uniform(0.22, 0.45)),
                        users_returning=int(visits * uniform(0.1, 0.25)),
                    )
                )


def bootstrap_data(db: Session) -> None:
    ensure_default_users(db)
    ensure_demo_metrics(db)
    db.commit()
