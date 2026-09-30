from datetime import datetime

from src.models import Metric


def test_metric_model():
    metric = Metric(
        timestamp=datetime.fromisoformat("2023-10-01T12:00:00+00:00"),
        cpu_usage=93,
        memory_usage=86,
        latency_ms=334,
        disk_usage=91,
        network_in_kbps=2000,
        network_out_kbps=1800,
        io_wait=12,
        thread_count=180,
        active_connections=130,
        error_rate=0.12,
        uptime_seconds=360000,
        temperature_celsius=84,
        power_consumption_watts=380,
        service_status={
            "database": "online",
            "api_gateway": "degraded",
            "cache": "online",
        },
    )

    assert metric.cpu_usage == 93
    assert metric.latency_ms == 334
    assert metric.service_status.database == "online"