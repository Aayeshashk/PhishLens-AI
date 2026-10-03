from pathlib import Path

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
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_FILE = (
    PROJECT_ROOT
    / "ml"
    / "dataset"
    / "url_features.csv"
)


def train_and_evaluate(
    X,
    y,
    feature_set_name,
):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                random_state=42,
            ),
        ),
    ])

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        y_pred,
    )

    precision = precision_score(
        y_test,
        y_pred,
        pos_label=0,
    )

    recall = recall_score(
        y_test,
        y_pred,
        pos_label=0,
    )

    f1 = f1_score(
        y_test,
        y_pred,
        pos_label=0,
    )

    return {
        "model": feature_set_name,
        "features": X.shape[1],
        "accuracy": accuracy,
        "phishing_precision": precision,
        "phishing_recall": recall,
        "phishing_f1": f1,
    }


def main():
    print("=" * 80)
    print("PHISHLENS AI — FEATURE ABLATION EXPERIMENT")
    print("=" * 80)

    print("\nLoading dataset...")

    df = pd.read_csv(DATASET_FILE)

    X = df.drop(
        columns=["label"]
    )

    y = df["label"]

    print(
        f"Dataset: {len(df)} rows, "
        f"{X.shape[1]} features"
    )

    results = []

    # -------------------------------------------------
    # MODEL A — CURRENT 34-FEATURE BASELINE
    # -------------------------------------------------

    results.append(
        train_and_evaluate(
            X,
            y,
            "A: All features",
        )
    )

    # -------------------------------------------------
    # MODEL B — REMOVE DIGIT + SLASH
    # -------------------------------------------------

    remove_b = [
        "digit_count",
        "slash_count",
    ]

    X_b = X.drop(
        columns=remove_b
    )

    results.append(
        train_and_evaluate(
            X_b,
            y,
            "B: Remove digit/slash",
        )
    )

    # -------------------------------------------------
    # MODEL C — REMOVE LENGTH + DIGIT + SLASH
    # -------------------------------------------------

    remove_c = [
        "digit_count",
        "slash_count",
        "path_length",
        "url_length",
    ]

    X_c = X.drop(
        columns=remove_c
    )

    results.append(
        train_and_evaluate(
            X_c,
            y,
            "C: Remove digit/slash/length",
        )
    )

    # -------------------------------------------------
    # DISPLAY RESULTS
    # -------------------------------------------------

    results_df = pd.DataFrame(results)

    print("\n")
    print("=" * 80)
    print("ABLATION RESULTS")
    print("=" * 80)

    print(
        results_df.to_string(
            index=False,
            formatters={
                "accuracy": "{:.4f}".format,
                "phishing_precision": "{:.4f}".format,
                "phishing_recall": "{:.4f}".format,
                "phishing_f1": "{:.4f}".format,
            },
        )
    )


if __name__ == "__main__":
    main()