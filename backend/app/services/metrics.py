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


def safe_div(num: float, den: float) -> float:
    return round(num / den, 4) if den else 0.0


def aggregate_metrics(rows: Iterable[MetricRow]) -> dict:
    visits = orders = users_new = users_returning = 0
    revenue = cost = 0.0

    for row in rows:
        visits += row.visits
        orders += row.orders
        revenue += row.revenue
        cost += row.cost
        users_new += row.users_new
        users_returning += row.users_returning

    conversion = safe_div(orders, visits)
    cac = safe_div(cost, orders)
    romi = safe_div((revenue - cost), cost)
    aov = safe_div(revenue, orders)
    retention = safe_div(users_returning, users_new + users_returning)
    ltv = round(aov * (1 + retention * 4), 2)

    return {
        "visits": visits,
        "orders": orders,
        "revenue": round(revenue, 2),
        "cost": round(cost, 2),
        "conversion": conversion,
        "cac": round(cac, 2),
        "romi": round(romi, 2),
        "aov": round(aov, 2),
        "retention": retention,
        "ltv": ltv,
    }
