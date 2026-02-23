# ВКР: Платформа аналитики маркетинга для ООО «Фабрика универсальных покрытий»

## Что это
Монорепозиторий с backend + frontend для аналитической обработки маркетинговых данных e-commerce:
- загрузка CSV/XLSX/JSON;
- коннекторы Яндекс.Метрика / Яндекс.Директ / VK Реклама (demo mode);
- единые метрики (conversion, CAC, ROMI, LTV, AOV, retention);
- прогнозы и аномалии;
- дашборды и таблицы;
- отчеты и история.

---

## Архитектура
- **Backend:** FastAPI, SQLAlchemy, Alembic, Celery, Redis, PostgreSQL.
- **Frontend:** React + TypeScript + Recharts + Vite.
- **Data layer:** `raw_events` (сырые) + `marketing_daily_metrics` (витрина).
- **Security:** JWT + роли (`admin`, `marketer`, `analyst`).

---

## Структура
```text
backend/
  app/
    api/
    connectors/
    core/
    db/
    models/
    schemas/
    services/
    tasks/
  alembic/
  scripts/
  tests/
  pyproject.toml
  requirements.txt
  .env.example
  run_dev.py

frontend/
  src/
  package.json
  .env.example

docker-compose.yml
scripts/bootstrap_pycharm.sh
```

---

## Запуск в PyCharm (рекомендуемый сценарий)

### Быстрый автоматический bootstrap
```bash
bash scripts/bootstrap_pycharm.sh
```

### Ручной запуск backend (PyCharm)
1. Открыть папку `backend` как Python проект.
2. Интерпретатор: `backend/.venv/bin/python`.
3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Создать `.env` из `.env.example`.
5. Поднять БД и Redis:
   ```bash
   docker compose up -d db redis
   ```
6. Применить миграции:
   ```bash
   alembic upgrade head
   ```
7. Наполнить демо-данными:
   ```bash
   python scripts/generate_demo_data.py
   ```
8. Запустить конфигурацию `backend/run_dev.py`.

### Ручной запуск frontend (PyCharm/WebStorm)
1. Открыть папку `frontend`.
2. Установить зависимости:
   ```bash
   npm install
   ```
3. Создать `.env` из `.env.example`.
4. Запустить:
   ```bash
   npm run dev
   ```

Frontend: http://127.0.0.1:5173  
Backend docs: http://127.0.0.1:8000/docs

---

## Docker Compose (полный запуск)
```bash
docker compose up --build
```

---

## Демо-учетки
- `admin@fup.ru / admin123`
- `marketer@fup.ru / marketer123`
- `analyst@fup.ru / analyst123`

---

## Тесты
```bash
cd backend
pytest
```

---

## Примечания по масштабированию
- индексы и SQL-агрегации уже включены в базовую модель;
- при росте данных: партиционирование витрины, materialized views, Redis-cache тяжелых запросов;
- для очень больших объемов можно заменить витрину на ClickHouse/TimescaleDB.
