from app.services.metrics import MetricRow, aggregate_metrics


def test_aggregate_metrics_basic():
    rows = [
        MetricRow(visits=100, orders=5, revenue=10000, cost=3000, users_new=50, users_returning=20),
        MetricRow(visits=200, orders=15, revenue=35000, cost=7000, users_new=80, users_returning=40),
    ]
    metrics = aggregate_metrics(rows)

    assert metrics["visits"] == 300
    assert metrics["orders"] == 20
    assert metrics["revenue"] == 45000
    assert metrics["cost"] == 10000
    assert metrics["conversion"] > 0
    assert metrics["romi"] > 0
