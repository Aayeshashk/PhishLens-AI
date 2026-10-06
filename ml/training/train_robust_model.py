from pathlib import Path

import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_DIR = (
    PROJECT_ROOT
    / "ml"
    / "dataset"
    / "robust_split"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "ml"
    / "models"
)

MODEL_FILE = (
    MODEL_DIR
    / "phishlens_robust_logistic_regression.joblib"
)


def load_split(filename: str):
    path = DATASET_DIR / filename

    df = pd.read_csv(path)

    X = df.drop(columns=["label"])
    y = df["label"]

    return X, y


def main() -> None:
    print("Loading robust training data...")

    X_train, y_train = load_split("train.csv")
    X_val, y_val = load_split("validation.csv")
    X_test, y_test = load_split("test.csv")

    print(f"Training rows:   {len(X_train):,}")
    print(f"Validation rows: {len(X_val):,}")
    print(f"Test rows:       {len(X_test):,}")

    print(f"\nFeatures: {X_train.shape[1]}")

    # ---------------------------------------------------------
    # Model
    #
    # Same model family as the original baseline:
    # StandardScaler + Logistic Regression
    # ---------------------------------------------------------

    model = Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    random_state=42,
                ),
            ),
        ]
    )

    print("\nTraining robust Logistic Regression...")

    model.fit(
        X_train,
        y_train,
    )

    # ---------------------------------------------------------
    # Validation evaluation
    # ---------------------------------------------------------

    print("\nValidation Results")

    validation_predictions = model.predict(
        X_val
    )

    print(
        f"Accuracy: "
        f"{accuracy_score(y_val, validation_predictions):.4f}"
    )

    print(
        "\nClassification report:"
    )

    print(
        classification_report(
            y_val,
            validation_predictions,
            target_names=[
                "phishing",
                "legitimate",
            ],
            digits=4,
        )
    )

    # ---------------------------------------------------------
    # Final test evaluation
    # ---------------------------------------------------------

    print("\nTest Results")

    test_predictions = model.predict(
        X_test
    )

    test_accuracy = accuracy_score(
        y_test,
        test_predictions,
    )

    print(
        f"Accuracy: {test_accuracy:.4f}"
    )

    print(
        "\nClassification report:"
    )

    print(
        classification_report(
            y_test,
            test_predictions,
            target_names=[
                "phishing",
                "legitimate",
            ],
            digits=4,
        )
    )

    print(
        "\nConfusion matrix:"
    )

    print(
        confusion_matrix(
            y_test,
            test_predictions,
        )
    )

    # ---------------------------------------------------------
    # Save model
    # ---------------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_FILE,
    )

    print(
        f"\nModel saved to:\n{MODEL_FILE}"
    )

    print(
        "\nPhase 7.3 training complete."
    )


if __name__ == "__main__":
    main()