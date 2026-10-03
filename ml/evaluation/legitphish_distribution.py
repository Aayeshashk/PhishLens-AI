import pandas as pd
from urllib.parse import urlparse


INPUT_FILE = (
    "ml/dataset/"
    "LegitPhish Dataset/"
    "LegitPhish Dataset/"
    "url_features_extracted1.csv"
)


def has_non_root_path(url):
    parsed = urlparse(str(url))
    return int(bool(parsed.path.strip("/")))


def main():
    print("=" * 90)
    print("PHISHLENS AI — LEGITPHISH DATASET ANALYSIS")
    print("=" * 90)

    print("\nLoading LegitPhish dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Total rows: {len(df)}")

    # Remove the one row without a class label.
    df = df.dropna(
        subset=["ClassLabel"]
    ).copy()

    df["ClassLabel"] = (
        df["ClassLabel"]
        .astype(int)
    )

    print(
        f"Rows after removing missing labels: "
        f"{len(df)}"
    )

    print("\nClass distribution:")

    print(
        df["ClassLabel"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nExtracting URL path information...")

    df["has_non_root_path"] = (
        df["URL"]
        .map(has_non_root_path)
    )

    print("\n")
    print("=" * 90)
    print("PATH PRESENCE BY CLASS")
    print("=" * 90)

    for label, name in [
        (0, "Phishing"),
        (1, "Legitimate"),
    ]:

        class_data = df[
            df["ClassLabel"] == label
        ]

        total = len(class_data)

        with_path = (
            class_data["has_non_root_path"] == 1
        ).sum()

        without_path = (
            class_data["has_non_root_path"] == 0
        ).sum()

        print(f"\n{name}:")
        print(f"Total:              {total}")
        print(
            f"With non-root path: {with_path}"
        )
        print(
            f"Without path:       {without_path}"
        )

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
    print("SAMPLE LEGITIMATE URLs WITH PATHS")
    print("=" * 90)

    legitimate_with_paths = df[
        (df["ClassLabel"] == 1)
        & (df["has_non_root_path"] == 1)
    ]

    print(
        legitimate_with_paths[
            "URL"
        ]
        .head(20)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()