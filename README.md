# ВКР: Платформа аналитики маркетинга (PyCharm-first)

Проект настроен так, чтобы вы **просто открыли папку `backend` в PyCharm и запустили `run_dev.py`**.

## Что происходит автоматически
- если Python-библиотеки не установлены, `run_dev.py` сам выполнит `pip install -r requirements.txt`;
- при старте приложения автоматически создается схема БД (SQLite локально);
- автоматически создаются пользователи и демо-данные (если БД пустая).

## Запуск (без Docker и без скриптов)
1. Откройте папку `backend` в PyCharm.
2. Выберите любой рабочий Python interpreter.
3. Запустите файл `run_dev.py`.

Готово.
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## Логины
- `admin@fup.ru / admin123`
- `marketer@fup.ru / marketer123`
- `analyst@fup.ru / analyst123`

## Frontend (опционально)
Если нужен UI:
1. Откройте `frontend` в PyCharm/WebStorm.
2. Выполните `npm install`.
3. Запустите `npm run dev`.

## Тесты
```bash
cd backend
pytest tests/test_metrics.py tests/test_insights.py
```

## Конфиг по умолчанию
- БД: `sqlite:///./analytics.db`
- Настройки можно переопределить через `.env` (шаблон: `backend/.env.example`).
