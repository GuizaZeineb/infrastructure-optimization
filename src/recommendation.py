from typing import Dict, List


def generate_recommendations(anomaly: Dict) -> List[Dict]:
    """Génère des recommandations à partir d'une anomalie."""

    if anomaly is None:
        return []

    if anomaly["severity"] == "high":
        return [
            {
                "id": "Recommendation-High-001",
                "action": "saturation",
                "target": "trafic",
                "parameters": {
                    "severity": "high"
                },
                "benefit_estimate": (
                    "Limiter immédiatement le trafic entrant afin de "
                    "préserver la disponibilité du système."
                ),
            },

            {
                "id": "Recommendation-High-002",
                "action": "saturation",
                "target": "compute",
                "parameters": {
                    "severity": "high"
                },
                "benefit_estimate": (
                    "Activer une mise à l'échelle horizontale afin de "
                    "répartir la charge entre plusieurs instances."
                ),
            }
        ]

    return [
        {
            "id": "Recommendation-Medium-001",
            "action": "pre-saturation",
            "target": "services",
            "parameters": {
                "severity": "medium"
            },
            "benefit_estimate": (
                "Désactiver temporairement les fonctionnalités "
                "secondaires afin de réduire la charge de traitement."
            ),
        },
        {
            "id": "Recommendation-Medium-002",
            "action": "pre-saturation",
            "target": "trafic",
            "parameters": {
                "severity": "medium"
            },
            "benefit_estimate": (
                 "Limiter temporairement le trafic entrant afin de contenir la "
                 "montée en charge et préserver la disponibilité du service principal."
 
            ),
        }

    ]