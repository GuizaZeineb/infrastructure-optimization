from src.recommendation import generate_recommendations


def test_no_recommendation_for_normal():
    assert generate_recommendations(None) == []


def test_medium_recommendation():
    anomaly = {
        "severity": "medium"
    }

    recommendations = generate_recommendations(anomaly)

    assert len(recommendations) == 2

    assert recommendations[0]["id"] == "Recommendation-Medium-001"
    assert recommendations[0]["action"]== "pre-saturation"
    assert recommendations[0]["target"]== "services"
    assert recommendations[0]["parameters"]["severity"] == "medium"
    
    assert recommendations[1]["id"] == "Recommendation-Medium-002"
    assert recommendations[1]["action"]== "pre-saturation"
    assert recommendations[1]["target"]== "trafic"
    assert recommendations[1]["parameters"]["severity"] == "medium"
 

def test_high_recommendation():
    anomaly = {
        "severity": "high"
    }

    recommendations = generate_recommendations(anomaly)
    
    assert len(recommendations) == 2

    assert recommendations[0]["id"] == "Recommendation-High-001"
    assert recommendations[0]["action"]== "saturation"
    assert recommendations[0]["target"]== "trafic"
    assert recommendations[0]["parameters"]["severity"] == "high"

    assert recommendations[1]["id"] == "Recommendation-High-002"
    assert recommendations[1]["action"]== "saturation"
    assert recommendations[1]["target"]== "compute"
    assert recommendations[1]["parameters"]["severity"] == "high"
