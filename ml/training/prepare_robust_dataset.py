from pathlib import Path

import pandas as pd

from ml.features.url_features import extract_url_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PHIUSIIL_FEATURES = (
    PROJECT_ROOT
    / "ml"
    / "dataset"
    / "url_features.csv"
)

LEGITIMATE_URLS = (
    PROJECT_ROOT
    / "ml"
    / "dataset"
    / "legitimate_urls.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "ml"
    / "dataset"
    / "robust_url_features.csv"
)


def normalize_url(url: str) -> str:
    """
    Normalize URLs for duplicate/overlap detection.

    This is only used for comparing URLs.
    The original URL values are not modified in the
    source datasets.
    """
    return str(url).strip().rstrip("/").lower()


def main() -> None:
    print("Loading PhiUSIIL feature dataset...")

    phi = pd.read_csv(PHIUSIIL_FEATURES)

    print(f"PhiUSIIL rows: {len(phi):,}")

    if "label" not in phi.columns:
        raise ValueError(
            "PhiUSIIL feature dataset does not contain 'label'."
        )

    print("\nLoading legitimate URL dataset...")

    legitimate = pd.read_csv(
        LEGITIMATE_URLS,
        usecols=["label", "url"],
    )

    print(
        f"Legitimate source rows: "
        f"{len(legitimate):,}"
    )

    if "url" not in legitimate.columns:
        raise ValueError(
            "Legitimate URL dataset does not contain 'url'."
        )

    # ---------------------------------------------------------
    # Normalize URLs for overlap detection
    # ---------------------------------------------------------

    print("\nChecking URL overlap...")

    phi_original = pd.read_csv(
        PROJECT_ROOT / "ml" / "dataset" / "phiusiil.csv",
        usecols=["URL"],
    )

    phi_urls = set(
        phi_original["URL"]
        .astype(str)
        .map(normalize_url)
    )

    legitimate["normalized_url"] = (
        legitimate["url"]
        .astype(str)
        .map(normalize_url)
    )

    overlap_mask = legitimate["normalized_url"].isin(
        phi_urls
    )

    overlap_count = int(overlap_mask.sum())

    print(
        f"Overlapping legitimate URLs removed: "
        f"{overlap_count:,}"
    )

    legitimate = legitimate.loc[
        ~overlap_mask
    ].copy()

    # ---------------------------------------------------------
    # Remove duplicate legitimate URLs
    # ---------------------------------------------------------

    before_duplicates = len(legitimate)

    legitimate = legitimate.drop_duplicates(
        subset=["normalized_url"]
    ).copy()

    duplicate_count = (
        before_duplicates - len(legitimate)
    )

    print(
        f"Duplicate legitimate URLs removed: "
        f"{duplicate_count:,}"
    )

    # ---------------------------------------------------------
    # Extract PhishLens features
    # ---------------------------------------------------------

    print("\nExtracting PhishLens features...")

    feature_rows = []

    for index, url in enumerate(
        legitimate["url"],
        start=1,
    ):
        feature_rows.append(
            extract_url_features(str(url))
        )

        if index % 25_000 == 0:
            print(
                f"Processed {index:,}/"
                f"{len(legitimate):,} URLs..."
            )

    legitimate_features = pd.DataFrame(
        feature_rows
    )

    # All URLs in this source are legitimate.
    legitimate_features["label"] = 1

    print(
        f"Extracted features for "
        f"{len(legitimate_features):,} URLs."
    )

    # ---------------------------------------------------------
    # Validate feature compatibility
    # ---------------------------------------------------------

    phi_feature_columns = [
        column
        for column in phi.columns
        if column != "label"
    ]

    legitimate_feature_columns = [
        column
        for column in legitimate_features.columns
        if column != "label"
    ]

    if phi_feature_columns != legitimate_feature_columns:
        raise ValueError(
            "Feature mismatch detected.\n\n"
            f"PhiUSIIL features:\n"
            f"{phi_feature_columns}\n\n"
            f"New legitimate features:\n"
            f"{legitimate_feature_columns}"
        )

    print("\nFeature compatibility check: PASSED")

    # ---------------------------------------------------------
    # Combine datasets
    # ---------------------------------------------------------

    robust = pd.concat(
        [
            phi[phi_feature_columns + ["label"]],
            legitimate_features[
                legitimate_feature_columns + ["label"]
            ],
        ],
        ignore_index=True,
    )

    # ---------------------------------------------------------
    # Final validation
    # ---------------------------------------------------------

    if robust.isna().any().any():
        raise ValueError(
            "NaN values detected in the robust dataset."
        )

    if len(robust.columns) != 35:
        raise ValueError(
            f"Expected 35 columns, "
            f"found {len(robust.columns)}."
        )

    print("\nFinal robust dataset:")
    print(f"Rows: {len(robust):,}")
    print(f"Columns: {len(robust.columns)}")

    print("\nFinal label distribution:")
    print(
        robust["label"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    print("\nSaving dataset...")

    robust.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print(
        f"\nSaved to:\n{OUTPUT_FILE}"
    )

    print("\nPhase 7.1 dataset preparation complete.")


if __name__ == "__main__":
    main()