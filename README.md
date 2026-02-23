# ВКР: Платформа аналитики маркетинга (без Docker)

Проект полностью ориентирован на **локальный запуск в PyCharm** без Docker.

## Стек
- Backend: FastAPI, SQLAlchemy, Alembic, Celery
- Frontend: React + TypeScript + Vite + Recharts
- БД по умолчанию: SQLite (локальный файл `backend/analytics.db`)
- Очереди: Celery (для локальной разработки можно не запускать worker)

## Структура
```text
backend/
  app/
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
```

## Быстрый запуск в PyCharm (без Docker)

### 1) Backend
1. Откройте папку `backend` в PyCharm.
2. Создайте интерпретатор `.venv`.
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Создайте `.env` из `.env.example`.
5. Выполните миграции:
   ```bash
   alembic upgrade head
   ```
6. Сгенерируйте демо-данные:
   ```bash
   python scripts/generate_demo_data.py
   ```
7. Запустите `run_dev.py`.

Backend: http://127.0.0.1:8000  
Swagger: http://127.0.0.1:8000/docs

### 2) Frontend
1. Откройте папку `frontend`.
2. Выполните:
   ```bash
   npm install
   ```
3. Создайте `.env` из `.env.example`.
4. Запустите:
   ```bash
   npm run dev
   ```

Frontend: http://127.0.0.1:5173

## Локальные пользователи
- `admin@fup.ru / admin123`
- `marketer@fup.ru / marketer123`
- `analyst@fup.ru / analyst123`

## Тесты
```bash
cd backend
pytest tests/test_metrics.py tests/test_insights.py
```

## Примечания
- Проект не требует Docker для работы.
- Для production можно подключить PostgreSQL и Redis через `.env`.
