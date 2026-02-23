from app.services.insights import detect_anomalies, forecast_linear


def test_forecast_linear_non_empty():
    out = forecast_linear([100, 110, 130, 150], 7)
    assert len(out) == 7


def test_detect_anomalies():
    out = detect_anomalies([10, 11, 9, 10, 45, 11, 10])
    assert 4 in out
