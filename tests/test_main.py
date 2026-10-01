import json

from src.main import run_pipeline


def test_pipeline_generates_expected_output(tmp_path):
    output_path = tmp_path / "output.json"

    run_pipeline("data/rapport.json", output_path)

    assert output_path.exists()

    with output_path.open("r", encoding="utf-8") as file:
        output = json.load(file)

    assert set(output.keys()) == {
        "timestamp",
        "insights",
        "anomalies",
        "recommendations",
        "service_status_summary",
    }


def test_insights_have_expected_fields(tmp_path):
    output_path = tmp_path / "output.json"

    run_pipeline("data/rapport.json", output_path)

    with output_path.open("r", encoding="utf-8") as file:
        output = json.load(file)

    assert set(output["insights"].keys()) == {
        "average_latency_ms",
        "max_cpu_usage",
        "max_memory_usage",
        "error_rate",
        "uptime_seconds",
    }


def test_anomalies_follow_expected_schema(tmp_path):
    output_path = tmp_path / "output.json"

    run_pipeline("data/rapport.json", output_path)

    with output_path.open("r", encoding="utf-8") as file:
        output = json.load(file)

    for anomaly in output["anomalies"]:
        assert set(anomaly.keys()) == {
            "metric",
            "value",
            "threshold",
            "severity",
            "description",
        }

        assert anomaly["severity"] in {"low", "medium", "high"}
        assert isinstance(anomaly["metric"], str)
        assert isinstance(anomaly["value"], (int, float))
        assert isinstance(anomaly["threshold"], (int, float))
        assert isinstance(anomaly["description"], str)


def test_service_status_summary_has_expected_structure(tmp_path):
    output_path = tmp_path / "output.json"

    run_pipeline("data/rapport.json", output_path)

    with output_path.open("r", encoding="utf-8") as file:
        output = json.load(file)

    assert set(output["service_status_summary"].keys()) == {
        "online",
        "degraded",
        "offline",
    }