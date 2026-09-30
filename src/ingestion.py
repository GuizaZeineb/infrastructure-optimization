import json
from pathlib import Path

from src.models import Metric
from typing import List, Union

#def load_metrics(file_path: str | Path) -> list[Metric]:
def load_metrics(file_path: Union[str, Path]) -> List[Metric]:
    """Charger et valider les mesures de l'infrastructure 
    à partir d'un fichier JSON."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [Metric.model_validate(item) for item in data]