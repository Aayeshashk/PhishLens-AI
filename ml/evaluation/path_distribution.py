import pandas as pd

from ml.features.url_features import extract_url_features


INPUT_FILE = "ml/dataset/phiusiil.csv"


def main():
    print("=" * 90)
    print("PHISHLENS AI — PATH DISTRIBUTION ANALYSIS")
    print("=" * 90)

    print("\nLoading dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Total rows: {len(df)}")

    print("\nExtracting path information...")

    rows = []

    for index, row in df.iterrows():

        if index % 25000 == 0:
            print(
                f"Processed {index} URLs..."
            )

        features = extract_url_features(
            str(row["URL"])
        )

        rows.append({
            "label": int(row["label"]),
            "has_path": int(
                features["slash_count"] > 0
            ),
        })

    feature_df = pd.DataFrame(rows)

    print("\n")
    print("=" * 90)
    print("PATH PRESENCE BY CLASS")
    print("=" * 90)

    for label, name in [
        (0, "Phishing"),
        (1, "Legitimate"),
    ]:

        class_data = feature_df[
            feature_df["label"] == label
        ]

        total = len(class_data)

        with_path = (
            class_data["has_path"] == 1
        ).sum()

        without_path = (
            class_data["has_path"] == 0
        ).sum()

        print(f"\n{name}:")
        print(f"Total:              {total}")
        print(f"With non-root path: {with_path}")
        print(f"Without path:       {without_path}")

        print(
            f"With path (%):      "
            f"{with_path / total * 100:.2f}%"
        )

        print(
            f"Without path (%):   "
            f"{without_path / total * 100:.2f}%"
        )

    print("\n")
    print("=" * 90)
    print("OVERALL")
    print("=" * 90)

    total_phishing = len(
        feature_df[
            feature_df["label"] == 0
        ]
    )

    total_legitimate = len(
        feature_df[
            feature_df["label"] == 1
        ]
    )

    phishing_with_path = (
        feature_df[
            (feature_df["label"] == 0)
            & (feature_df["has_path"] == 1)
        ]
        .shape[0]
    )

    legitimate_with_path = (
        feature_df[
            (feature_df["label"] == 1)
            & (feature_df["has_path"] == 1)
        ]
        .shape[0]
    )

    print(
        f"Phishing path rate: "
        f"{phishing_with_path / total_phishing * 100:.2f}%"
    )

    print(
        f"Legitimate path rate: "
        f"{legitimate_with_path / total_legitimate * 100:.2f}%"
    )


if __name__ == "__main__":
    main()