from src.analysis import compute_insights
from src.ingestion import load_metrics


def test_compute_insights():
    metrics = load_metrics("data/rapport.json")

    insights = compute_insights(metrics)

    assert round(insights["average_latency_ms"], 2) == 156.02
    assert insights["max_cpu_usage"] == 99
    assert insights["max_memory_usage"] == 92
    assert round(insights["error_rate"], 5) == 0.03158
    assert insights["uptime_seconds"] == 1258200