from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "phishlens_logistic_regression.joblib"
)


def main():
    print("=" * 80)
    print("PHISHLENS AI — MODEL FEATURE ANALYSIS")
    print("=" * 80)

    print("\nLoading model...")

    model = joblib.load(MODEL_FILE)

    classifier = model.named_steps["classifier"]

    feature_names = list(
        model.feature_names_in_
    )

    coefficients = classifier.coef_[0]

    feature_importance = pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefficients,
    })

    feature_importance["absolute"] = (
        feature_importance["coefficient"]
        .abs()
    )

    feature_importance = feature_importance.sort_values(
        "absolute",
        ascending=False,
    )

    print("\nTop features by absolute coefficient:")
    print("-" * 80)

    for _, row in feature_importance.head(20).iterrows():
        print(
            f"{row['feature']:<35}"
            f"{row['coefficient']:>15.6f}"
        )

    print("\n")
    print("Coefficient interpretation:")
    print(
        "Positive coefficient → pushes prediction toward "
        "legitimate (label 1)."
    )
    print(
        "Negative coefficient → pushes prediction toward "
        "phishing (label 0)."
    )


if __name__ == "__main__":
    main()