from datetime import datetime, timezone

from src.episode_detector import detect_episodes
from src.models import Metric, ServiceStatus


def create_metric(timestamp, cpu_usage, latency_ms):
    return Metric(
        timestamp=datetime.fromisoformat(timestamp).replace(tzinfo=timezone.utc),
        cpu_usage=cpu_usage,
        memory_usage=65,
        latency_ms=latency_ms,
        disk_usage=60,
        network_in_kbps=1000,
        network_out_kbps=1000,
        io_wait=3,
        thread_count=150,
        active_connections=50,
        error_rate=0.02,
        uptime_seconds=500000,
        temperature_celsius=60,
        power_consumption_watts=250,
        service_status=ServiceStatus(
            database="online",
            api_gateway="online",
            cache="online",
        ),
    )


def test_detect_medium_episode():
    metrics = [
        create_metric("2023-10-01T12:00:00", 55, 130),
        create_metric("2023-10-01T12:30:00", 70, 180),
        create_metric("2023-10-01T13:00:00", 72, 190),
        create_metric("2023-10-01T13:30:00", 55, 130),
    ]

    episodes = detect_episodes(metrics)

    assert len(episodes) == 1
    assert episodes[0]["severity"] == "medium"
    assert episodes[0]["measurements_count"] == 2


def test_detect_high_episode():
    metrics = [
        create_metric("2023-10-01T12:00:00", 55, 130),
        create_metric("2023-10-01T12:30:00", 90, 320),
        create_metric("2023-10-01T13:00:00", 95, 350),
        create_metric("2023-10-01T13:30:00", 55, 130),
    ]

    episodes = detect_episodes(metrics)

    assert len(episodes) == 1
    assert episodes[0]["severity"] == "high"
    assert episodes[0]["measurements_count"] == 2


def test_episode_ends_when_regime_returns_to_normal():
    metrics = [
        create_metric("2023-10-01T12:00:00", 70, 180),
        create_metric("2023-10-01T12:30:00", 72, 190),
        create_metric("2023-10-01T13:00:00", 55, 130),
        create_metric("2023-10-01T13:30:00", 71, 185),
    ]

    episodes = detect_episodes(metrics)

    assert len(episodes) == 2
    assert episodes[0]["severity"] == "medium"
    assert episodes[0]["measurements_count"] == 2
    assert episodes[1]["severity"] == "medium"
    assert episodes[1]["measurements_count"] == 1


def test_episode_is_split_when_severity_changes():
    metrics = [
        create_metric("2023-10-01T12:00:00", 70, 180),
        create_metric("2023-10-01T12:30:00", 90, 320),
        create_metric("2023-10-01T13:00:00", 95, 350),
    ]

    episodes = detect_episodes(metrics)

    assert len(episodes) == 2

    assert episodes[0]["severity"] == "medium"
    assert episodes[0]["measurements_count"] == 1

    assert episodes[1]["severity"] == "high"
    assert episodes[1]["measurements_count"] == 2


def test_no_episode_for_normal_metrics():
    metrics = [
        create_metric("2023-10-01T12:00:00", 55, 130),
        create_metric("2023-10-01T12:30:00", 56, 135),
    ]

    episodes = detect_episodes(metrics)

    assert episodes == []