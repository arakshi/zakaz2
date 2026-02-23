from datetime import date, timedelta
import statistics


def compare_periods(current: dict, previous: dict) -> list[str]:
    comments: list[str] = []
    for key in ("revenue", "orders", "conversion", "cost"):
        cur = current.get(key, 0)
        prev = previous.get(key, 0)
        if prev == 0:
            continue
        diff = ((cur - prev) / prev) * 100
        if abs(diff) > 5:
            trend = "вырос" if diff > 0 else "снизился"
            comments.append(f"Показатель {key} {trend} на {abs(diff):.1f}%")
    return comments


def detect_anomalies(values: list[float], threshold: float = 2.0) -> list[int]:
    if len(values) < 5:
        return []
    mean = statistics.mean(values)
    std = statistics.pstdev(values) or 1
    return [idx for idx, value in enumerate(values) if abs((value - mean) / std) >= threshold]


def forecast_linear(history: list[float], horizon_days: int) -> list[float]:
    if not history:
        return [0.0] * horizon_days
    n = len(history)
    x = list(range(n))
    x_mean = statistics.mean(x)
    y_mean = statistics.mean(history)
    num = sum((x[i] - x_mean) * (history[i] - y_mean) for i in range(n))
    den = sum((x[i] - x_mean) ** 2 for i in range(n)) or 1
    slope = num / den
    intercept = y_mean - slope * x_mean
    return [round(intercept + slope * (n + step), 2) for step in range(1, horizon_days + 1)]


def build_forecast_dates(start: date, horizon_days: int) -> list[str]:
    return [(start + timedelta(days=i)).isoformat() for i in range(1, horizon_days + 1)]


def budget_recommendations(channels: list[dict]) -> list[str]:
    recommendations: list[str] = []
    sorted_channels = sorted(channels, key=lambda c: c.get("romi", 0), reverse=True)
    if len(sorted_channels) < 2:
        return ["Недостаточно данных для рекомендаций"]
    best = sorted_channels[0]
    worst = sorted_channels[-1]
    if best.get("romi", 0) > worst.get("romi", 0):
        recommendations.append(
            f"Рекомендуется перераспределить 10-15% бюджета из {worst['channel']} в {best['channel']}"
        )
    return recommendations or ["Текущая структура бюджета сбалансирована"]
