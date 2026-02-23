import json
from pathlib import Path

import pandas as pd


SUPPORTED_EXT = {".csv", ".xlsx", ".xls", ".json"}


def parse_uploaded_file(path: str) -> list[dict]:
    p = Path(path)
    ext = p.suffix.lower()
    if ext not in SUPPORTED_EXT:
        raise ValueError(f"Неподдерживаемый формат: {ext}. Разрешены: {sorted(SUPPORTED_EXT)}")

    if ext == ".csv":
        return pd.read_csv(p).to_dict(orient="records")
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(p).to_dict(orient="records")

    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
