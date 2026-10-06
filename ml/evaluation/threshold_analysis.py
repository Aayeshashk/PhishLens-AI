from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TEST_FILE = (
    PROJECT_ROOT
    / "ml"
    / "dataset"
    / "robust_split"
    / "test.csv"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "phishlens_robust_logistic_regression.joblib"
)


THRESHOLDS = [
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
    0.65,
    0.70,
]


def evaluate_threshold(
    threshold: float,
    probabilities,
    y_true,
) -> dict:

    # Probability index 0 = phishing
    phishing_probability = probabilities[:, 0]

    # Predict phishing when phishing probability
    # reaches the selected threshold.
    predictions = (
        phishing_probability >= threshold
    ).astype(int)

    # Our labels are:
    # 0 = phishing
    # 1 = legitimate
    #
    # Therefore convert boolean phishing predictions
    # into the project label format.
    predictions = 1 - predictions

    accuracy = accuracy_score(
        y_true,
        predictions,
    )

    phishing_precision = precision_score(
        y_true,
        predictions,
        pos_label=0,
        zero_division=0,
    )

    phishing_recall = recall_score(
        y_true,
        predictions,
        pos_label=0,
        zero_division=0,
    )

    phishing_f1 = f1_score(
        y_true,
        predictions,
        pos_label=0,
        zero_division=0,
    )

    legitimate_recall = recall_score(
        y_true,
        predictions,
        pos_label=1,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_true,
        predictions,
    )

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

    return {
        "threshold": threshold,
        "accuracy": accuracy,
        "phishing_precision": phishing_precision,
        "phishing_recall": phishing_recall,
        "phishing_f1": phishing_f1,
        "legitimate_recall": legitimate_recall,
        "false_positive_rate": false_positive_rate,
        "false_negative_rate": false_negative_rate,
    }


def main():
    print("=" * 110)
    print("PHISHLENS AI — ROBUST MODEL THRESHOLD ANALYSIS")
    print("=" * 110)

    print("\nLoading test dataset...")

    test_df = pd.read_csv(TEST_FILE)

    X_test = test_df.drop(
        columns=["label"]
    )

    y_test = test_df["label"]

    print(f"Test rows: {len(test_df):,}")
    print(f"Features: {X_test.shape[1]}")

    print("\nLoading robust model...")

    model = joblib.load(
        MODEL_FILE
    )

    print("Generating probability predictions...")

    probabilities = model.predict_proba(
        X_test
    )

    print("\nEvaluating thresholds...")

    results = []

    for threshold in THRESHOLDS:
        result = evaluate_threshold(
            threshold,
            probabilities,
            y_test,
        )

        results.append(result)

    results_df = pd.DataFrame(results)

    display_df = results_df.copy()

    percentage_columns = [
        "accuracy",
        "phishing_precision",
        "phishing_recall",
        "phishing_f1",
        "legitimate_recall",
        "false_positive_rate",
        "false_negative_rate",
    ]

    for column in percentage_columns:
        display_df[column] = (
            display_df[column] * 100
        ).round(2)

    print("\n" + "=" * 110)
    print("THRESHOLD RESULTS")
    print("=" * 110)

    print(
        display_df.to_string(
            index=False
        )
    )

    best_f1_index = results_df[
        "phishing_f1"
    ].idxmax()

    best_f1 = results_df.loc[
        best_f1_index
    ]

    lowest_fpr_index = results_df[
        "false_positive_rate"
    ].idxmin()

    lowest_fpr = results_df.loc[
        lowest_fpr_index
    ]

    print("\n" + "=" * 110)
    print("BEST PHISHING F1 THRESHOLD")
    print("=" * 110)

    print(
        f"Threshold: "
        f"{best_f1['threshold']:.2f}"
    )

    print(
        f"Phishing F1: "
        f"{best_f1['phishing_f1'] * 100:.2f}%"
    )

    print(
        f"Phishing Recall: "
        f"{best_f1['phishing_recall'] * 100:.2f}%"
    )

    print(
        f"False Positive Rate: "
        f"{best_f1['false_positive_rate'] * 100:.2f}%"
    )

    print("\n" + "=" * 110)
    print("LOWEST FALSE-POSITIVE RATE")
    print("=" * 110)

    print(
        f"Threshold: "
        f"{lowest_fpr['threshold']:.2f}"
    )

    print(
        f"False Positive Rate: "
        f"{lowest_fpr['false_positive_rate'] * 100:.2f}%"
    )

    print(
        f"Phishing Recall: "
        f"{lowest_fpr['phishing_recall'] * 100:.2f}%"
    )

    print("\nThreshold analysis complete.")


if __name__ == "__main__":
    main()