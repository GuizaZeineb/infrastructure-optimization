from src.ingestion import load_metrics


def test_load_metrics():
    metrics = load_metrics("data/rapport.json")

    assert len(metrics) == 500
    assert metrics[0].cpu_usage == 93
    assert metrics[0].latency_ms == 334