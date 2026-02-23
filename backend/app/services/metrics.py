from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class MetricRow:
    visits: int
    orders: int
    revenue: float
    cost: float
    users_new: int
    users_returning: int


def _safe_div(num: float, den: float) -> float:
    return (num / den) if den else 0.0


def aggregate_metrics(rows: Iterable[MetricRow]) -> dict:
    total = MetricRow(0, 0, 0.0, 0.0, 0, 0)
    for row in rows:
        total.visits += row.visits
        total.orders += row.orders
        total.revenue += row.revenue
        total.cost += row.cost
        total.users_new += row.users_new
        total.users_returning += row.users_returning

    conversion = _safe_div(total.orders, total.visits)
    cac = _safe_div(total.cost, total.orders)
    romi = _safe_div((total.revenue - total.cost), total.cost)
    aov = _safe_div(total.revenue, total.orders)
    retention = _safe_div(total.users_returning, total.users_new + total.users_returning)

    return {
        "visits": total.visits,
        "orders": total.orders,
        "revenue": round(total.revenue, 2),
        "cost": round(total.cost, 2),
        "conversion": round(conversion, 4),
        "cac": round(cac, 2),
        "romi": round(romi, 2),
        "aov": round(aov, 2),
        "retention": round(retention, 4),
        "ltv": round(aov * (1 + retention * 4), 2),
    }
