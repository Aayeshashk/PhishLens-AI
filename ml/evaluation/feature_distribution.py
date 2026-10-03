import pandas as pd

from ml.features.url_features import extract_url_features


INPUT_FILE = "ml/dataset/phiusiil.csv"


def main():
    print("=" * 90)
    print("PHISHLENS AI — FEATURE DISTRIBUTION ANALYSIS")
    print("=" * 90)

    print("\nLoading dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Rows: {len(df)}")

    print("\nExtracting selected features...")

    rows = []

    for index, row in df.iterrows():

        if index % 25000 == 0:
            print(
                f"Processed {index} URLs..."
            )

        url = str(row["URL"])

        features = extract_url_features(url)

        rows.append({
            "label": int(row["label"]),
            "slash_count": features["slash_count"],
            "path_length": features["path_length"],
            "url_length": features["url_length"],
            "suspicious_keyword_count":
                features["suspicious_keyword_count"],
        })

    feature_df = pd.DataFrame(rows)

    print("\n")
    print("=" * 90)
    print("AVERAGE FEATURE VALUES BY CLASS")
    print("=" * 90)

    grouped = feature_df.groupby("label")[
        [
            "slash_count",
            "path_length",
            "url_length",
            "suspicious_keyword_count",
        ]
    ].mean()

    grouped.index = [
        "Phishing (0)"
        if label == 0
        else "Legitimate (1)"
        for label in grouped.index
    ]

    print(
        grouped.to_string(
            float_format=lambda value:
                f"{value:.3f}"
        )
    )

    print("\n")
    print("=" * 90)
    print("SLASH COUNT DISTRIBUTION")
    print("=" * 90)

    slash_distribution = (
        feature_df
        .groupby(
            ["label", "slash_count"]
        )
        .size()
        .reset_index(
            name="count"
        )
    )

    for label in [0, 1]:

        class_name = (
            "Phishing"
            if label == 0
            else "Legitimate"
        )

        print(
            f"\n{class_name}:"
        )

        class_data = slash_distribution[
            slash_distribution["label"] == label
        ].copy()

        total = class_data["count"].sum()

        class_data["percentage"] = (
            class_data["count"]
            / total
            * 100
        )

        print(
            class_data[
                [
                    "slash_count",
                    "count",
                    "percentage",
                ]
            ]
            .head(15)
            .to_string(
                index=False,
                formatters={
                    "percentage":
                        "{:.2f}%".format
                },
            )
        )


if __name__ == "__main__":
    main()