from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIREMENTS = ROOT / "requirements.txt"

REQUIRED_IMPORTS = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "jose",
    "passlib",
    "pydantic",
]


def ensure_dependencies() -> None:
    missing = [pkg for pkg in REQUIRED_IMPORTS if importlib.util.find_spec(pkg) is None]
    if not missing:
        return

    print(f"[bootstrap] Installing missing packages: {', '.join(missing)}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)])


def main() -> None:
    ensure_dependencies()

    from uvicorn import run

    run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
