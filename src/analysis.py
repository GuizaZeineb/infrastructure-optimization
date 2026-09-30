from typing import List

from src.models import Metric


def compute_insights(metrics: List[Metric]) -> dict:
    """Calcule les statistiques globales sur les mesures."""

    return {

        "average_latency_ms": sum(
            metric.latency_ms for metric in metrics
        ) / len(metrics),

        "max_cpu_usage": max(
            metric.cpu_usage for metric in metrics
        ),

        "max_memory_usage": max(
            metric.memory_usage for metric in metrics
        ),

        "error_rate": sum(
            metric.error_rate for metric in metrics
        ) / len(metrics),
        
        "uptime_seconds": max(
            metric.uptime_seconds for metric in metrics
        ),
    }