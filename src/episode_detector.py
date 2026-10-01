from typing import Dict, List

from src.anomaly_detector import detect_regime
from src.models import Metric


def detect_episodes(metrics: List[Metric]) -> List[Dict]:
    """Regroupe les mesures contigues appartenant au même régime dégradé."""

    episodes = []
    current_episode = None

    for metric in metrics:
        regime = detect_regime(metric.model_dump())

        """Si le régime est normal, clôturer l'épisode 
        "anormal en cours (s'il y en a un) et l'enregistre."""

        if regime == "normal":
            if current_episode is not None:
                episodes.append(current_episode)
                current_episode = None
            continue


        """Si une anomalie apparaît et qu'aucun épisode n'est 
        actif, démarrer un nouveau avec le timestamp 
        de début et un compteur à 1."""

        if current_episode is None:
            current_episode = {
                "severity": regime,
                "start_timestamp": metric.timestamp,
                "end_timestamp": metric.timestamp,
                "measurements_count": 1,
            }
            continue

        """ Si l'anomalie continue avec la même gravité (même régime), 
        mettre à jour le timestamp de fin et incrémente le nombre de mesures.
        Si le type d'anomalie change, sauvegarder l'épisode actuel 
        et créer un nouveau pour le nouveau régime."""

        if current_episode["severity"] == regime:
            current_episode["end_timestamp"] = metric.timestamp
            current_episode["measurements_count"] += 1
        else:
            episodes.append(current_episode)

            current_episode = {
                "severity": regime,
                "start_timestamp": metric.timestamp,
                "end_timestamp": metric.timestamp,
                "measurements_count": 1,
            }

    if current_episode is not None:
        episodes.append(current_episode)

    return episodes