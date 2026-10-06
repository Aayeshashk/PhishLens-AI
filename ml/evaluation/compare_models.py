from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TEST_FILE = (
    PROJECT_ROOT
    / "ml"
    / "dataset"
    / "robust_split"
    / "test.csv"
)

BASELINE_MODEL_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "phishlens_logistic_regression.joblib"
)

ROBUST_MODEL_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "phishlens_robust_logistic_regression.joblib"
)


def evaluate_model(name, model, X_test, y_test):
    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    phishing_precision = precision_score(
        y_test,
        predictions,
        pos_label=0,
        zero_division=0,
    )

    phishing_recall = recall_score(
        y_test,
        predictions,
        pos_label=0,
        zero_division=0,
    )

    phishing_f1 = f1_score(
        y_test,
        predictions,
        pos_label=0,
        zero_division=0,
    )

    legitimate_precision = precision_score(
        y_test,
        predictions,
        pos_label=1,
        zero_division=0,
    )

    legitimate_recall = recall_score(
        y_test,
        predictions,
        pos_label=1,
        zero_division=0,
    )

    legitimate_f1 = f1_score(
        y_test,
        predictions,
        pos_label=1,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
    )

    # Matrix format:
    #
    # [[true_phishing, false_legitimate],
    #  [false_phishing, true_legitimate]]
    #
    # Since label 0 = phishing and label 1 = legitimate:
    #
    # False positive = legitimate URL predicted as phishing.
    # False negative = phishing URL predicted as legitimate.

    true_phishing = matrix[0, 0]
    false_negative = matrix[0, 1]
    false_positive = matrix[1, 0]
    true_legitimate = matrix[1, 1]

    false_positive_rate = (
        false_positive
        / (false_positive + true_legitimate)
    )

    false_negative_rate = (
        false_negative
        / (false_negative + true_phishing)
    )

    print("\n" + "=" * 90)
    print(name.upper())
    print("=" * 90)

    print(f"Accuracy:              {accuracy:.4f}")
    print(
        f"Phishing Precision:    "
        f"{phishing_precision:.4f}"
    )
    print(
        f"Phishing Recall:       "
        f"{phishing_recall:.4f}"
    )
    print(
        f"Phishing F1:           "
        f"{phishing_f1:.4f}"
    )

    print(
        f"Legitimate Precision:  "
        f"{legitimate_precision:.4f}"
    )
    print(
        f"Legitimate Recall:     "
        f"{legitimate_recall:.4f}"
    )
    print(
        f"Legitimate F1:         "
        f"{legitimate_f1:.4f}"
    )

    print(
        f"\nFalse Positive Rate:    "
        f"{false_positive_rate:.4f}"
        f" ({false_positive_rate * 100:.2f}%)"
    )

    print(
        f"False Negative Rate:    "
        f"{false_negative_rate:.4f}"
        f" ({false_negative_rate * 100:.2f}%)"
    )

    print("\nConfusion Matrix:")
    print(matrix)

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=[
                "phishing",
                "legitimate",
            ],
            digits=4,
        )
    )

    return {
        "accuracy": accuracy,
        "phishing_precision": phishing_precision,
        "phishing_recall": phishing_recall,
        "phishing_f1": phishing_f1,
        "legitimate_precision": legitimate_precision,
        "legitimate_recall": legitimate_recall,
        "legitimate_f1": legitimate_f1,
        "false_positive_rate": false_positive_rate,
        "false_negative_rate": false_negative_rate,
    }


def main():
    print("=" * 90)
    print("PHISHLENS AI — BASELINE VS ROBUST MODEL COMPARISON")
    print("=" * 90)

    print("\nLoading robust held-out test set...")

    test_df = pd.read_csv(TEST_FILE)

    X_test = test_df.drop(
        columns=["label"]
    )

    y_test = test_df["label"]

    print(f"Test rows: {len(test_df):,}")
    print(f"Features: {X_test.shape[1]}")

    print("\nLoading baseline model...")
    baseline_model = joblib.load(
        BASELINE_MODEL_FILE
    )

    print("Loading robust model...")
    robust_model = joblib.load(
        ROBUST_MODEL_FILE
    )

    baseline_results = evaluate_model(
        "Baseline Logistic Regression",
        baseline_model,
        X_test,
        y_test,
    )

    robust_results = evaluate_model(
        "Robust Logistic Regression",
        robust_model,
        X_test,
        y_test,
    )

    print("\n" + "=" * 90)
    print("FINAL COMPARISON")
    print("=" * 90)

    comparison = pd.DataFrame(
        {
            "Baseline": baseline_results,
            "Robust": robust_results,
        }
    )

    print(
        comparison.round(4).to_string()
    )

    print("\n" + "=" * 90)
    print("METRIC DIFFERENCE — ROBUST MINUS BASELINE")
    print("=" * 90)

    difference = (
        pd.Series(robust_results)
        - pd.Series(baseline_results)
    )

    print(
        difference.round(4).to_string()
    )

    print("\nComparison complete.")


if __name__ == "__main__":
    main()