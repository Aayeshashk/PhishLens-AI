from pathlib import Path

import joblib
import pandas as pd

from ml.features.url_features import extract_url_features
from ml.services.risk_engine import calculate_risk


# Project root:
# PhishLens-AI/
# ├── ml/
# │   └── services/
# │       └── prediction_service.py
#
# parents[0] = services
# parents[1] = ml
# parents[2] = PhishLens-AI

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "phishlens_logistic_regression.joblib"
)


class PhishLensPredictor:

    def __init__(self):
        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                f"PhishLens model not found at: {MODEL_FILE}"
            )

        self.model = joblib.load(MODEL_FILE)

    def predict(self, url: str) -> dict:

        # Extract URL features
        features = extract_url_features(url)

        # Convert features into DataFrame
        feature_df = pd.DataFrame([features])

        # ML prediction
        probabilities = self.model.predict_proba(
            feature_df
        )[0]

        # Dataset convention:
        # 0 = phishing
        # 1 = legitimate

        phishing_probability = float(
            probabilities[0]
        )

        legitimate_probability = float(
            probabilities[1]
        )

        # Hybrid risk analysis
        risk_result = calculate_risk(
            phishing_probability,
            features,
        )

        return {
            "url": url,
            "classification": risk_result[
                "classification"
            ],
            "risk_score": risk_result[
                "risk_score"
            ],
            "phishing_probability": round(
                phishing_probability,
                4,
            ),
            "legitimate_probability": round(
                legitimate_probability,
                4,
            ),
            "indicators": risk_result[
                "indicators"
            ],
        }