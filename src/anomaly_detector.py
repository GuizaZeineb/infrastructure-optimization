# Seuils identifiés à partir de l'EDA pour distinguer
# les trois régimes de fonctionnement observés.

THRESHOLDS = {
    "medium": {
        "cpu_usage": 65,
        "latency_ms": 165,
    },
    "high": {
        "cpu_usage": 85,
        "latency_ms": 277,
    },
}


def detect_regime(metrics):
    """ Classer une mesure selon qu'elle indique une dégradation normale, moyenne ou élevée."""
    if (
        metrics["cpu_usage"] >= THRESHOLDS["high"]["cpu_usage"]
        and metrics["latency_ms"] >= THRESHOLDS["high"]["latency_ms"]
    ):
        return "high"

    if (
        metrics["cpu_usage"] >= THRESHOLDS["medium"]["cpu_usage"]
        and metrics["latency_ms"] >= THRESHOLDS["medium"]["latency_ms"]
    ):
        return "medium"

    return "normal"


def detect_anomaly(metrics):
    regime = detect_regime(metrics)

    if regime == "normal":
        return None

    if regime == "medium":
        severity = "medium"
        description = (
            "Moderate system degradation detected "
            "based on CPU usage and latency."
        )
    else:
        severity = "high"
        description = (
            "High system degradation detected "
            "based on CPU usage and latency."
        )

    return {
        "metric": "cpu_latency",
        "value": {
            "cpu_usage": metrics["cpu_usage"],
            "latency_ms": metrics["latency_ms"],
        },
        "threshold": {
            "cpu_usage": THRESHOLDS[regime]["cpu_usage"],
            "latency_ms": THRESHOLDS[regime]["latency_ms"],
        },
        "severity": severity,
        "description": description,
    }

