import pandas as pd
from urllib.parse import urlparse


INPUT_FILE = (
    "ml/dataset/"
    "LegitPhish Dataset/"
    "LegitPhish Dataset/"
    "url_features_extracted1.csv"
)


def get_domain(url):
    return urlparse(
        str(url)
    ).netloc.lower()


def has_non_root_path(url):
    parsed = urlparse(str(url))
    return int(
        bool(
            parsed.path.strip("/")
        )
    )


def main():
    print("=" * 90)
    print("PHISHLENS AI — LEGITPHISH PATH DIVERSITY ANALYSIS")
    print("=" * 90)

    print("\nLoading dataset...")

    df = pd.read_csv(INPUT_FILE)

    df = df.dropna(
        subset=["ClassLabel"]
    ).copy()

    df["ClassLabel"] = (
        df["ClassLabel"]
        .astype(int)
    )

    legitimate_paths = df[
        (df["ClassLabel"] == 1)
        & (
            df["URL"].map(
                has_non_root_path
            ) == 1
        )
    ].copy()

    print(
        f"\nLegitimate URLs with paths: "
        f"{len(legitimate_paths)}"
    )

    legitimate_paths["domain"] = (
        legitimate_paths["URL"]
        .map(get_domain)
    )

    print("\n")
    print("=" * 90)
    print("DOMAIN DIVERSITY")
    print("=" * 90)

    unique_domains = (
        legitimate_paths["domain"]
        .nunique()
    )

    unique_urls = (
        legitimate_paths["URL"]
        .nunique()
    )

    print(
        f"Unique legitimate URLs: "
        f"{unique_urls}"
    )

    print(
        f"Unique domains: "
        f"{unique_domains}"
    )

    print("\n")
    print("=" * 90)
    print("TOP DOMAINS")
    print("=" * 90)

    domain_counts = (
        legitimate_paths["domain"]
        .value_counts()
        .head(20)
    )

    print(
        domain_counts.to_string()
    )

    print("\n")
    print("=" * 90)
    print("DUPLICATE ANALYSIS")
    print("=" * 90)

    duplicate_count = (
        len(legitimate_paths)
        - legitimate_paths["URL"].nunique()
    )

    print(
        f"Duplicate URL rows: "
        f"{duplicate_count}"
    )

    print("\n")
    print("=" * 90)
    print("SAMPLE URLS FROM DIFFERENT DOMAINS")
    print("=" * 90)

    sample = (
        legitimate_paths
        .drop_duplicates(
            subset=["domain"]
        )
        [["domain", "URL"]]
        .head(30)
    )

    print(
        sample.to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()