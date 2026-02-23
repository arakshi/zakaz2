from datetime import date, timedelta
from statistics import mean, pstdev


def compare_periods(current: dict, previous: dict) -> list[str]:
    messages: list[str] = []
    for metric in ["revenue", "orders", "conversion", "cost"]:
        prev = previous.get(metric, 0)
        cur = current.get(metric, 0)
        if not prev:
            continue
        delta = ((cur - prev) / prev) * 100
        if abs(delta) >= 5:
            direction = "рост" if delta > 0 else "падение"
            messages.append(f"{metric}: {direction} на {abs(delta):.1f}%")
    return messages


def detect_anomalies(series: list[float], z: float = 2.0) -> list[int]:
    if len(series) < 5:
        return []
    m, s = mean(series), pstdev(series) or 1
    return [i for i, v in enumerate(series) if abs((v - m) / s) >= z]


def forecast_linear(history: list[float], days: int) -> list[float]:
    if not history:
        return [0.0] * days
    n = len(history)
    x_mean = (n - 1) / 2
    y_mean = mean(history)
    numerator = sum((i - x_mean) * (y - y_mean) for i, y in enumerate(history))
    denominator = sum((i - x_mean) ** 2 for i in range(n)) or 1
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    return [round(intercept + slope * (n + i), 2) for i in range(1, days + 1)]


def forecast_dates(last_day: date, days: int) -> list[str]:
    return [(last_day + timedelta(days=i)).isoformat() for i in range(1, days + 1)]


def recommend_budget(channels: list[dict]) -> list[str]:
    if len(channels) < 2:
        return ["Недостаточно данных для рекомендаций"]
    sorted_by_romi = sorted(channels, key=lambda x: x.get("romi", 0), reverse=True)
    best, worst = sorted_by_romi[0], sorted_by_romi[-1]
    if best["channel"] == worst["channel"]:
        return ["Структура бюджета стабильна"]
    return [f"Перераспределите 10% бюджета из «{worst['channel']}» в «{best['channel']}». "]
