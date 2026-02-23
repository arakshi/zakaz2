from __future__ import annotations

import importlib.util
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version
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
    "email_validator",
    "bcrypt",
]

PINNED_VERSIONS = {
    "bcrypt": "4.0.1",
    "passlib": "1.7.4",
}


def ensure_dependencies() -> None:
    missing = [pkg for pkg in REQUIRED_IMPORTS if importlib.util.find_spec(pkg) is None]

    wrong_versions: list[str] = []
    for pkg, expected in PINNED_VERSIONS.items():
        try:
            current = version(pkg)
        except PackageNotFoundError:
            missing.append(pkg)
            continue
        if current != expected:
            wrong_versions.append(f"{pkg}=={expected} (current: {current})")

    if not missing and not wrong_versions:
        return

    if missing:
        print(f"[bootstrap] Installing missing packages: {', '.join(sorted(set(missing)))}")
    if wrong_versions:
        print(f"[bootstrap] Fixing versions: {', '.join(wrong_versions)}")

    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "--force-reinstall", "bcrypt==4.0.1", "passlib==1.7.4"])


def main() -> None:
    ensure_dependencies()

    from uvicorn import run

    run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
