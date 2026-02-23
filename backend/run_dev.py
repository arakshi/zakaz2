"""Single entrypoint for PyCharm.

Откройте папку backend в PyCharm и запустите этот файл.
Если зависимости не установлены — скрипт установит их автоматически,
после чего запустит приложение.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIREMENTS = ROOT / "requirements.txt"


def ensure_dependencies() -> None:
    fastapi_installed = importlib.util.find_spec("fastapi") is not None
    if fastapi_installed:
        return

    print("[bootstrap] Устанавливаю зависимости...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])  # nosec B603
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)])  # nosec B603


def main() -> None:
    ensure_dependencies()

    from uvicorn import run

    run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
