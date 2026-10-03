from ml.services.prediction_service import PhishLensPredictor


def main():
    predictor = PhishLensPredictor()

    legitimate_urls = [
        "https://github.com/login",
        "https://github.com/explore",
        "https://github.com/features",
        "https://www.google.com/search",
        "https://www.google.com/maps",
        "https://www.microsoft.com/en-us/",
        "https://www.microsoft.com/en-us/account",
        "https://www.amazon.com/gp/help",
        "https://www.amazon.com/account",
        "https://stackoverflow.com/questions",
        "https://stackoverflow.com/users",
        "https://www.wikipedia.org/wiki/Computer",
        "https://www.python.org/downloads/",
        "https://docs.python.org/3/",
        "https://www.nasa.gov/missions/",
    ]

    print("=" * 100)
    print("PHISHLENS AI — REALISTIC LEGITIMATE URL EVALUATION")
    print("=" * 100)

    print(
        "\nThese URLs are being treated as legitimate examples "
        "for stress-testing the current model."
    )

    print("\n")

    false_positives = 0

    for url in legitimate_urls:

        result = predictor.predict(url)

        is_false_positive = (
            result["classification"] != "safe"
        )

        if is_false_positive:
            false_positives += 1

        print("-" * 100)

        print(f"URL: {url}")

        print(
            f"Classification: "
            f"{result['classification']}"
        )

        print(
            f"Risk Score: "
            f"{result['risk_score']}/100"
        )

        print(
            f"Phishing Probability: "
            f"{result['phishing_probability']:.4f}"
        )

        print(
            f"Legitimate Probability: "
            f"{result['legitimate_probability']:.4f}"
        )

        print(
            f"False Positive: "
            f"{'YES' if is_false_positive else 'NO'}"
        )

    total = len(legitimate_urls)

    false_positive_rate = (
        false_positives / total
    ) * 100

    print("\n")
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)

    print(
        f"Total legitimate test URLs: {total}"
    )

    print(
        f"Predicted as safe: "
        f"{total - false_positives}"
    )

    print(
        f"Predicted as suspicious/phishing: "
        f"{false_positives}"
    )

    print(
        f"False-positive rate: "
        f"{false_positive_rate:.2f}%"
    )

    print("\n")
    print(
        "Important: This is an external stress test, "
        "not part of the original PhiUSIIL test split."
    )


if __name__ == "__main__":
    main()