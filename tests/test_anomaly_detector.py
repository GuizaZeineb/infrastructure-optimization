from src.anomaly_detector import detect_regime, detect_anomaly

def test_normal_regime():
    metrics = {
        "cpu_usage": 60,
        "latency_ms": 130,
    }
    assert detect_regime(metrics) == "normal"


def test_medium_regime():
    metrics = {
        "cpu_usage": 70,
        "latency_ms": 200,
    }

    assert detect_regime(metrics)=="medium"



def test_high_regime():
    metrics = {
        "cpu_usage": 93,
        "latency_ms": 334,
    }

    assert detect_regime(metrics) == "high"



def test_no_anomaly_for_normal_regime():
        metrics = {
        "cpu_usage": 60,
        "latency_ms": 130,
    }
        
        assert detect_anomaly(metrics) is None

def test_high_anomaly():
    metrics = {
        "cpu_usage": 93,
        "latency_ms": 334,
    }

    anomaly = detect_anomaly(metrics)

    assert anomaly["severity"] == "high"
    assert anomaly["metric"] == "cpu_latency"
    assert anomaly["value"]["cpu_usage"] == 93


