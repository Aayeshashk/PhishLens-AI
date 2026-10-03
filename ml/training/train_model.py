import os

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)


INPUT_FILE = "ml/dataset/url_features.csv"
MODEL_FILE = "ml/models/phishlens_logistic_regression.joblib"


def main():

    print("Loading feature dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Dataset shape: {df.shape}")

    # Separate features and target
    X = df.drop(columns=["label"])
    y = df["label"]

    print("\nClass distribution:")
    print(y.value_counts())

    # Train / test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("\nData split:")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    # Pipeline:
    # 1. Standardize features
    # 2. Train Logistic Regression
    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    print("\nTraining Logistic Regression...")

    model.fit(X_train, y_train)

    print("Training complete.")

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)

    # Important:
    # label 0 = phishing
    # label 1 = legitimate
    #
    # We calculate phishing metrics explicitly.
    phishing_precision = precision_score(
        y_test,
        y_pred,
        pos_label=0,
    )

    phishing_recall = recall_score(
        y_test,
        y_pred,
        pos_label=0,
    )

    phishing_f1 = f1_score(
        y_test,
        y_pred,
        pos_label=0,
    )

    print("\n" + "=" * 50)
    print("PHISHLENS AI — BASELINE MODEL RESULTS")
    print("=" * 50)

    print(f"Accuracy:           {accuracy:.4f}")
    print(f"Phishing Precision: {phishing_precision:.4f}")
    print(f"Phishing Recall:    {phishing_recall:.4f}")
    print(f"Phishing F1:        {phishing_f1:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "Phishing",
                "Legitimate",
            ],
        )
    )

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Save model
    os.makedirs("ml/models", exist_ok=True)

    joblib.dump(model, MODEL_FILE)

    print("\nModel saved to:")
    print(MODEL_FILE)


if __name__ == "__main__":
    main()