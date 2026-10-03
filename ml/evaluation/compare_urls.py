from pathlib import Path

import joblib
import pandas as pd

from ml.features.url_features import extract_url_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "phishlens_logistic_regression.joblib"
)


def get_model_components(model):
    """
    Extract the scaler and logistic regression classifier
    from the trained pipeline.
    """

    scaler = model.named_steps["scaler"]
    classifier = model.named_steps["classifier"]

    return scaler, classifier


def calculate_feature_contributions(
    model,
    features,
):
    """
    Calculate the contribution of every feature to the
    logistic regression decision score.

    Contribution =
        standardized feature value × model coefficient
    """

    scaler, classifier = get_model_components(model)

    feature_names = list(features.keys())

    feature_df = pd.DataFrame(
        [features],
        columns=feature_names,
    )

    scaled_values = scaler.transform(
        feature_df
    )[0]

    coefficients = classifier.coef_[0]

    contributions = []

    for index, feature_name in enumerate(
        feature_names
    ):

        contribution = (
            scaled_values[index]
            * coefficients[index]
        )

        contributions.append(
            {
                "feature": feature_name,
                "value": features[feature_name],
                "scaled_value": scaled_values[index],
                "coefficient": coefficients[index],
                "contribution": contribution,
            }
        )

    return contributions


def print_contributions(
    url,
    model,
):
    features = extract_url_features(url)

    contributions = calculate_feature_contributions(
        model,
        features,
    )

    contributions.sort(
        key=lambda item: abs(
            item["contribution"]
        ),
        reverse=True,
    )

    decision = model.decision_function(
        pd.DataFrame([features])
    )[0]

    probabilities = model.predict_proba(
        pd.DataFrame([features])
    )[0]

    print("\n")
    print("=" * 100)
    print(f"URL: {url}")
    print("=" * 100)

    print(
        f"Phishing probability: "
        f"{probabilities[0]:.4f}"
    )

    print(
        f"Legitimate probability: "
        f"{probabilities[1]:.4f}"
    )

    print(
        f"Decision score: "
        f"{decision:.4f}"
    )

    print("\nTop feature contributions:")
    print("-" * 100)

    print(
        f"{'Feature':<35}"
        f"{'Value':>10}"
        f"{'Coefficient':>15}"
        f"{'Contribution':>18}"
    )

    print("-" * 80)

    for item in contributions[:15]:

        print(
            f"{item['feature']:<35}"
            f"{str(item['value']):>10}"
            f"{item['coefficient']:>15.4f}"
            f"{item['contribution']:>18.4f}"
        )


def main():

    print("=" * 100)
    print("PHISHLENS AI — FEATURE CONTRIBUTION ANALYSIS")
    print("=" * 100)

    print("\nLoading model...")

    model = joblib.load(
        MODEL_FILE
    )

    print("Model loaded successfully.")

    urls = [
        "https://example.com",
        "https://example.com/login",
        "https://example.com/account",
        "https://example.com/account/verify/password",
    ]

    for url in urls:
        print_contributions(
            url,
            model,
        )


if __name__ == "__main__":
    main()