"""Локальный запуск backend из PyCharm.

Использование:
1) Создайте .env из .env.example
2) Поднимите PostgreSQL и Redis (например, docker compose up db redis)
3) Выполните alembic upgrade head
4) Запустите этот файл из PyCharm
"""

import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
