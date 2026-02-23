from app.services.metrics import MetricRow, aggregate_metrics


def test_aggregate_metrics():
    rows = [
        MetricRow(visits=100, orders=5, revenue=12000, cost=3000, users_new=45, users_returning=10),
        MetricRow(visits=200, orders=8, revenue=24000, cost=7000, users_new=90, users_returning=20),
    ]
    result = aggregate_metrics(rows)
    assert result["visits"] == 300
    assert result["orders"] == 13
    assert result["revenue"] == 36000
    assert result["romi"] > 0
