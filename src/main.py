import json
from pathlib import Path
from typing import Dict, List

from src.analysis import compute_insights
from src.anomaly_detector import THRESHOLDS
from src.episode_detector import detect_episodes
from src.ingestion import load_metrics
from src.recommendation import generate_recommendations


def build_anomaly(episode: Dict, metrics: List) -> Dict:
    """Transforme un épisode interne en anomalie conforme au format attendu."""

    episode_metrics = [
        metric
        for metric in metrics
        if episode["start_timestamp"] <= metric.timestamp <= episode["end_timestamp"]
    ]

    peak_metric = max(episode_metrics, key=lambda metric: metric.cpu_usage)

    severity = episode["severity"]

    description = (
        f"Dégradation {severity} détectée sur "
        f"{episode['measurements_count']} mesure(s), "
        f"de {episode['start_timestamp'].isoformat()} "
        f"à {episode['end_timestamp'].isoformat()}. "
        f"La détection repose sur l'utilisation CPU et la latence."
    )

    return {
        "metric": "cpu_usage",
        "value": peak_metric.cpu_usage,
        "threshold": THRESHOLDS[severity]["cpu_usage"],
        "severity": severity,
        "description": description,
    }


def build_service_status_summary(metric) -> Dict[str, List[str]]:
    """Construit le résumé des services à partir de la dernière mesure."""

    summary = {
        "online": [],
        "degraded": [],
        "offline": [],
    }

    services = metric.service_status.model_dump()

    for service, status in services.items():
        if status in summary:
            summary[status].append(service)

    return summary


def run_pipeline(data_path: Path, output_path: Path) -> None:

    metrics = load_metrics(data_path)

    """statistiques globales"""
    insights = compute_insights(metrics)

    episodes = detect_episodes(metrics)

    anomalies = [
        build_anomaly(episode, metrics)
        for episode in episodes
    ]

    recommendations = []

    for anomaly in anomalies:
        recommendations.extend(
            generate_recommendations(anomaly)
        )

    # Évite les recommandations dupliquées lorsque plusieurs
    # épisodes ont la même sévérité.
    unique_recommendations = list(
        {recommendation["id"]: recommendation for recommendation in recommendations}.values()
    )

    output = {
        "timestamp": metrics[-1].timestamp.isoformat(),
        "insights": insights,
        "anomalies": anomalies,
        "recommendations": unique_recommendations,
        "service_status_summary": build_service_status_summary(metrics[-1]),
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2, ensure_ascii=False)


def main() -> None:
    run_pipeline(
        Path("data/rapport.json"),
        Path("output.json"),
    )

if __name__ == "__main__":
    main()