from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "ml"
    / "dataset"
    / "robust_url_features.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "ml"
    / "dataset"
    / "robust_split"
)

RANDOM_STATE = 42


def main() -> None:
    print("Loading robust dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Total rows: {len(df):,}")

    phishing = df[df["label"] == 0].copy()
    legitimate = df[df["label"] == 1].copy()

    print(f"Phishing rows: {len(phishing):,}")
    print(f"Legitimate rows: {len(legitimate):,}")

    # ---------------------------------------------------------
    # Balance the classes for model development.
    #
    # We keep all phishing examples and randomly sample the
    # same number of legitimate examples.
    # ---------------------------------------------------------

    legitimate_sample = legitimate.sample(
        n=len(phishing),
        random_state=RANDOM_STATE,
    )

    balanced = pd.concat(
        [
            phishing,
            legitimate_sample,
        ],
        ignore_index=True,
    )

    # ---------------------------------------------------------
    # Create stratified train/test split.
    # ---------------------------------------------------------

    train_df, test_df = train_test_split(
        balanced,
        test_size=0.20,
        stratify=balanced["label"],
        random_state=RANDOM_STATE,
    )

    # ---------------------------------------------------------
    # Create validation split from training data.
    #
    # 20% of the original data is test.
    # Of the remaining 80%, 20% becomes validation.
    # Final proportions:
    #
    # Train: 64%
    # Validation: 16%
    # Test: 20%
    # ---------------------------------------------------------

    train_df, val_df = train_test_split(
        train_df,
        test_size=0.20,
        stratify=train_df["label"],
        random_state=RANDOM_STATE,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    train_file = OUTPUT_DIR / "train.csv"
    val_file = OUTPUT_DIR / "validation.csv"
    test_file = OUTPUT_DIR / "test.csv"

    train_df.to_csv(
        train_file,
        index=False,
    )

    val_df.to_csv(
        val_file,
        index=False,
    )

    test_df.to_csv(
        test_file,
        index=False,
    )

    print("\nSplit complete.")

    print("\nTrain:")
    print(f"Rows: {len(train_df):,}")
    print(
        train_df["label"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    print("\nValidation:")
    print(f"Rows: {len(val_df):,}")
    print(
        val_df["label"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    print("\nTest:")
    print(f"Rows: {len(test_df):,}")
    print(
        test_df["label"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    print("\nSaved:")
    print(train_file)
    print(val_file)
    print(test_file)


if __name__ == "__main__":
    main()