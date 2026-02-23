# ВКР-проект: Платформа маркетинговой аналитики e-commerce

## 1. Архитектура
Монорепозиторий включает:
- **backend** (FastAPI + PostgreSQL + Celery + Redis) — API, расчет метрик, прогнозы, отчеты, интеграции.
- **frontend** (React + TypeScript + Recharts) — русскоязычный SaaS-интерфейс с дашбордами.
- **docker-compose** — единый запуск всех сервисов.

### Ключевые принципы
- Чистая архитектура: `api -> services -> repositories/models`.
- Сырые события (`raw_events`) + витрина (`marketing_daily_metrics`).
- Инкрементальные обновления через `merge` и уникальные ключи по дате/каналу/кампании.
- Масштабирование: индексы, агрегации в SQL, готовность к кэшу и фоновым задачам.
- Demo mode: заглушки интеграций и генератор реалистичных данных без API-ключей.

## 2. Структура проекта
```text
zakaz2/
  backend/
    app/
      api/
      connectors/
      core/
      db/
      models/
      repositories/
      schemas/
      services/
      tasks/
    alembic/
      versions/
    scripts/
    tests/
    .env.example
    pytest.ini
    run_dev.py
    Dockerfile
    requirements.txt
  frontend/
    src/
      api/
      components/
      layouts/
      pages/
      types/
    .env.example
    Dockerfile
    package.json
  docker-compose.yml
  README.md
```

## 3. Реализованный функционал
- Загрузка данных из **CSV/XLSX/JSON**.
- Коннекторы: **Яндекс Метрика**, **Яндекс Директ**, **VK Реклама**, универсальный импорт.
- Метрики: conversion, CAC, ROMI, LTV, AOV, retention.
- Сравнение периодов и автокомментарии.
- Детектирование аномалий и линейный прогноз на 7/30/90 дней.
- Рекомендации по перераспределению бюджета (white-hat логика).
- JWT авторизация, роли: `admin`, `marketer`, `analyst`.
- Аудит-таблица под ключевые операции.
- Отчеты: шаблоны + генерация HTML + история.

## 4. Миграции и схема БД
- Alembic миграция `20261001_0001_init.py` создает таблицы:
  - `users`
  - `raw_events`
  - `marketing_daily_metrics`
  - `report_templates`
  - `generated_reports`
  - `audit_logs`

## 5. Демо-данные
Скрипт `backend/scripts/generate_demo_data.py` создает:
- Администратора: `admin@fup.ru / admin123`
- 180 дней реалистичных маркетинговых данных по каналам и кампаниям.

## 6. Маршруты интерфейса
- `/` Дашборд
- `/channels` Каналы
- `/campaigns` Кампании
- `/funnel` Воронка
- `/cohorts` Когорты
- `/forecast` Прогноз
- `/reports` Отчеты
- `/integrations` Интеграции
- `/settings` Настройки

## 7. Запуск одной командой (Docker)
```bash
docker compose up --build
```

После запуска:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs

---

## 8. Запуск в PyCharm (рекомендуется для разработки)

### Backend
1. Откройте папку `backend` как Python-проект в PyCharm.
2. Создайте venv и установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте `.env` из `.env.example`.
4. Поднимите инфраструктуру (минимум Postgres + Redis):
   ```bash
   docker compose up -d db redis
   ```
5. Примените миграции:
   ```bash
   alembic upgrade head
   ```
6. Сгенерируйте демо-данные:
   ```bash
   python scripts/generate_demo_data.py
   ```
7. Запустите backend прямо из PyCharm файлом `run_dev.py`.

### Frontend
1. Откройте папку `frontend` как Node-проект в PyCharm/WebStorm.
2. Установите зависимости:
   ```bash
   npm install
   ```
3. Создайте `.env` из `.env.example`.
4. Запуск:
   ```bash
   npm run dev
   ```

## 9. Тестирование
```bash
cd backend
pytest
```

`backend/pytest.ini` уже настроен для корректного `PYTHONPATH` в PyCharm.

## 10. Нагрузочные заметки и ограничения
- Для production рекомендуется:
  - вынести celery beat + periodic jobs;
  - использовать TimescaleDB/ClickHouse для сверхбольших историй;
  - добавить Redis-кэш результатов тяжелых агрегатов;
  - внедрить партиционирование `marketing_daily_metrics` по месяцам.
