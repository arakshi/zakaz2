import json
import pandas as pd
from pathlib import Path


def parse_uploaded_file(path: str) -> list[dict]:
    file_path = Path(path)
    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path).to_dict(orient="records")
    if file_path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(file_path).to_dict(orient="records")
    if file_path.suffix.lower() == ".json":
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    raise ValueError("Поддерживаются только CSV, XLSX и JSON")
