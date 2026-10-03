import sys
from pathlib import Path


# Add the project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from ml.services.prediction_service import PhishLensPredictor


def test_predictor_loads_model():
    predictor = PhishLensPredictor()

    assert predictor.model is not None


def test_predictor_returns_prediction():
    predictor = PhishLensPredictor()

    result = predictor.predict(
        "https://www.google.com"
    )

    assert isinstance(result, dict)

    assert "url" in result
    assert "classification" in result
    assert "risk_score" in result
    assert "phishing_probability" in result
    assert "legitimate_probability" in result
    assert "indicators" in result


def test_predictor_safe_url():
    predictor = PhishLensPredictor()

    result = predictor.predict(
        "https://www.google.com"
    )

    assert result["classification"] == "safe"

    assert (
        result["legitimate_probability"]
        > result["phishing_probability"]
    )


def test_predictor_phishing_url():
    predictor = PhishLensPredictor()

    result = predictor.predict(
        "http://secure-login-example.com/verify/account"
    )

    assert result["classification"] == "phishing"

    assert (
        result["phishing_probability"]
        > result["legitimate_probability"]
    )


def test_predictor_probabilities_are_valid():
    predictor = PhishLensPredictor()

    result = predictor.predict(
        "https://www.google.com"
    )

    phishing_probability = result[
        "phishing_probability"
    ]

    legitimate_probability = result[
        "legitimate_probability"
    ]

    assert 0 <= phishing_probability <= 1
    assert 0 <= legitimate_probability <= 1

    assert abs(
        phishing_probability
        + legitimate_probability
        - 1.0
    ) < 0.0001