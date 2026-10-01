# Infrastructure Optimization

Application Python permettant d'analyser des métriques d'infrastructure, de détecter des épisodes de dégradation et de générer des recommandations.

## Fonctionnement

Le traitement se fait en plusieurs étapes :

1. Les données sont chargées depuis le fichier rapport.json.
2. Les données sont validées avec Pydantic.
3. Les statistiques globales sont calculées.
4. Les épisodes de dégradation sont détectés à partir du CPU et de la latence.
5. Des recommandations sont générées en fonction de la sévérité détectée.
6. Le résultat est écrit dans output.json.

## Détection des anomalies

L'analyse exploratoire a montré que l'utilisation CPU et la latence évoluent fortement lors des périodes de dégradation.

Les seuils utilisés sont :

* medium : CPU >= 65 et latence >= 165 ms
* high : CPU >= 85 et latence >= 277 ms

Les deux métriques sont utilisées conjointement pour éviter de considérer une variation isolée comme une anomalie.

Les autres métriques sont conservées dans les données et permettent de donner du contexte aux périodes détectées. Elles sont aussi bien corrélées aux métriques principales.

## Épisodes de dégradation

Les mesures dégradées qui se suivent dans le temps sont regroupées en épisodes.

Une anomalie représente donc un épisode de dégradation et non simplement une mesure isolée.

Pour chaque épisode, la sortie indique notamment :

* la sévérité ;
* le nombre de mesures concernées ;
* le début de l'épisode ;
* la fin de l'épisode.

## Recommandations

Les recommandations sont actuellement basées sur des règles simples en fonction de la sévérité de l'anomalie.

Les recommandations identiques sont dédupliquées dans la sortie finale.

## Format de sortie

Le programme génère un fichier output.json contenant :

* timestamp : date de la dernière mesure analysée ;
* insights : statistiques globales ;
* anomalies : épisodes de dégradation détectés ;
* recommendations : actions proposées ;
* service_status_summary : état des services lors de la dernière mesure.

## Installation

Installer les dépendances :

pip install -r requirements.txt

## Exécution

Depuis la racine du projet :

python -m src.main


Le fichier output.json est généré à la racine du projet.

## Tests

Les tests peuvent être exécutés avec :

pytest


Les tests couvrent les différents modules ainsi que le fonctionnement global du pipeline.

## Analyse exploratoire

L'analyse exploratoire se trouve dans :

notebooks/01_eda.ipynb


Elle permet notamment d'observer les distributions des métriques, leur évolution dans le temps, les corrélations entre métriques et les différents régimes présents dans les données.

## Structure du projet

```text
data/         
    rapport.json         

notebooks/         
    01_eda.ipynb         

src/         
    analysis.py         
    anomaly_detector.py         
    episode_detector.py         
    ingestion.py         
    main.py         
    models.py         
    recommendation.py         

tests/         
    test_analysis.py         
    test_anomaly_detector.py         
    test_episode_detector.py         
    test_ingestion.py         
    test_main.py 
    test_models.py         
    test_recommendation.py         
            

output.json 
pyproject.toml
README.md        
requirements.txt         
         

```

