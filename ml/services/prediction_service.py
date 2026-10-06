from pathlib import Path

import joblib
import pandas as pd

from ml.features.url_features import extract_url_features
from ml.services.risk_engine import calculate_risk


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "phishlens_robust_logistic_regression.joblib"
)

PHISHING_THRESHOLD = 0.55


def build_explainable_signals(features: dict) -> list[dict]:
    """
    Convert extracted URL features into human-readable
    security signals for explainable analysis.
    """

    signals = []

    # HTTPS
    if features["has_https"] == 1:
        signals.append(
            {
                "name": "HTTPS",
                "value": "Enabled",
                "interpretation": "The URL uses encrypted HTTPS communication.",
                "severity": "low",
            }
        )
    else:
        signals.append(
            {
                "name": "HTTPS",
                "value": "Not used",
                "interpretation": "The URL does not use encrypted HTTPS communication.",
                "severity": "medium",
            }
        )

    # IP address
    if features["has_ip_address"] == 1:
        signals.append(
            {
                "name": "IP Address",
                "value": "Detected",
                "interpretation": (
                    "The URL uses an IP address instead of a conventional "
                    "domain name, which can be suspicious."
                ),
                "severity": "high",
            }
        )
    else:
        signals.append(
            {
                "name": "IP Address",
                "value": "Not detected",
                "interpretation": "The URL uses a domain name rather than a raw IP address.",
                "severity": "low",
            }
        )

    # @ symbol
    if features["has_at_symbol"] == 1:
        signals.append(
            {
                "name": "@ Symbol",
                "value": "Detected",
                "interpretation": (
                    "The URL contains an '@' symbol, which can be used "
                    "to obscure the actual destination."
                ),
                "severity": "high",
            }
        )
    else:
        signals.append(
            {
                "name": "@ Symbol",
                "value": "Not detected",
                "interpretation": "No '@' symbol was detected in the URL.",
                "severity": "low",
            }
        )

    # URL length
    url_length = features["url_length"]

    if url_length > 100:
        length_severity = "medium"
        length_interpretation = (
            "The URL is unusually long and may contain additional "
            "elements intended to obscure its destination."
        )
    elif url_length > 75:
        length_severity = "low"
        length_interpretation = "The URL is moderately long."
    else:
        length_severity = "low"
        length_interpretation = "The URL length is within a normal range."

    signals.append(
        {
            "name": "URL Length",
            "value": f"{url_length} characters",
            "interpretation": length_interpretation,
            "severity": length_severity,
        }
    )

    # Subdomains
    subdomain_count = features["subdomain_count"]

    if subdomain_count >= 3:
        signals.append(
            {
                "name": "Subdomains",
                "value": str(subdomain_count),
                "interpretation": (
                    "The URL contains an unusually high number of "
                    "subdomains, which may increase suspicion."
                ),
                "severity": "medium",
            }
        )
    else:
        signals.append(
            {
                "name": "Subdomains",
                "value": str(subdomain_count),
                "interpretation": "The number of subdomains is within a typical range.",
                "severity": "low",
            }
        )

    # Suspicious keywords
    keyword_count = features["suspicious_keyword_count"]

    if keyword_count >= 2:
        signals.append(
            {
                "name": "Security Keywords",
                "value": str(keyword_count),
                "interpretation": (
                    "Multiple security-sensitive keywords were detected "
                    "in the URL."
                ),
                "severity": "medium",
            }
        )
    elif keyword_count == 1:
        signals.append(
            {
                "name": "Security Keywords",
                "value": "1",
                "interpretation": (
                    "One security-sensitive keyword was detected "
                    "in the URL."
                ),
                "severity": "low",
            }
        )
    else:
        signals.append(
            {
                "name": "Security Keywords",
                "value": "None",
                "interpretation": (
                    "No security-sensitive keywords were detected "
                    "in the URL."
                ),
                "severity": "low",
            }
        )

    # Query parameters
    query_parameter_count = features["query_parameter_count"]

    signals.append(
        {
            "name": "Query Parameters",
            "value": str(query_parameter_count),
            "interpretation": (
                "Number of query parameters detected in the URL."
            ),
            "severity": "low",
        }
    )

    # Special characters
    special_character_count = (
        features["at_count"]
        + features["question_mark_count"]
        + features["equal_count"]
        + features["ampersand_count"]
        + features["percent_count"]
    )

    if special_character_count >= 5:
        signals.append(
            {
                "name": "Special Characters",
                "value": str(special_character_count),
                "interpretation": (
                    "The URL contains a relatively high number of "
                    "special characters."
                ),
                "severity": "medium",
            }
        )
    else:
        signals.append(
            {
                "name": "Special Characters",
                "value": str(special_character_count),
                "interpretation": (
                    "No unusually high concentration of special "
                    "characters was detected."
                ),
                "severity": "low",
            }
        )

    return signals


class PhishLensPredictor:
    def __init__(self):
        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                f"PhishLens model not found at: {MODEL_FILE}"
            )

        self.model = joblib.load(MODEL_FILE)

        if not hasattr(self.model, "predict_proba"):
            raise TypeError(
                "Loaded PhishLens model does not support probability predictions."
            )

    def predict(self, url: str) -> dict:
        if not isinstance(url, str):
            raise TypeError("URL must be provided as a string.")

        url = url.strip()

        if not url:
            raise ValueError("URL cannot be empty.")

        features = extract_url_features(url)

        feature_df = pd.DataFrame([features])

        probabilities = self.model.predict_proba(feature_df)[0]

        if len(probabilities) < 2:
            raise ValueError(
                "PhishLens model returned an invalid probability output."
            )

        phishing_probability = float(probabilities[0])
        legitimate_probability = float(probabilities[1])

        if not (0.0 <= phishing_probability <= 1.0):
            raise ValueError(
                "Invalid phishing probability returned by the model."
            )

        if not (0.0 <= legitimate_probability <= 1.0):
            raise ValueError(
                "Invalid legitimate probability returned by the model."
            )

        probability_sum = (
            phishing_probability + legitimate_probability
        )

        if abs(probability_sum - 1.0) > 0.0001:
            raise ValueError(
                "Model probabilities do not sum to 1."
            )

        ml_is_phishing = (
            phishing_probability >= PHISHING_THRESHOLD
        )

        risk_result = calculate_risk(
            phishing_probability,
            features,
        )

        classification = risk_result["classification"]

        if ml_is_phishing:
            classification = "phishing"

        signals = build_explainable_signals(features)

        return {
            "url": url,
            "classification": classification,
            "risk_score": risk_result["risk_score"],
            "phishing_probability": round(
                phishing_probability,
                4,
            ),
            "legitimate_probability": round(
                legitimate_probability,
                4,
            ),
            "indicators": risk_result["indicators"],
            "signals": signals,
        }