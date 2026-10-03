import pandas as pd

from ml.features.url_features import extract_url_features


INPUT_FILE = "ml/dataset/phiusiil.csv"
OUTPUT_FILE = "ml/dataset/url_features.csv"


def main():
    print("Loading dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Total rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    # Keep only the information we need initially
    data = df[["URL", "label"]].copy()

    # Remove missing URLs
    data = data.dropna(subset=["URL"])

    print(f"Rows after removing missing URLs: {len(data)}")

    print("\nExtracting URL features...")

    feature_rows = []

    for index, row in data.iterrows():
        if index % 10000 == 0:
            print(f"Processed {index} URLs...")

        features = extract_url_features(str(row["URL"]))
        features["label"] = int(row["label"])

        feature_rows.append(features)

    features_df = pd.DataFrame(feature_rows)

    features_df.to_csv(OUTPUT_FILE, index=False)

    print("\nFeature extraction complete.")
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"Rows: {len(features_df)}")
    print(f"Features: {len(features_df.columns) - 1}")

    print("\nLabel distribution:")
    print(features_df["label"].value_counts())


if __name__ == "__main__":
    main()