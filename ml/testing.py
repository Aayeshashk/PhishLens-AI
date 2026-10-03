from ml.services.prediction_service import PhishLensPredictor


def main():
    predictor = PhishLensPredictor()

    test_urls = [
        "https://www.google.com",
        "https://example.com",
        "https://example.com/login",
        "https://example.com/account",
        "https://example.com/account/verify/password",
        "http://secure-login-example.com/verify/account",
        "http://192.168.1.100/login",
        "http://google.com@evil-example.com/login",
        "https://example.com/" + "a" * 120,
    ]

    print("=" * 80)
    print("PHISHLENS AI — PREDICTION SANITY CHECK")
    print("=" * 80)

    for url in test_urls:
        result = predictor.predict(url)

        print("\nURL:")
        print(url)

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
            f"Indicators: "
            f"{len(result['indicators'])}"
        )

        print("-" * 80)


if __name__ == "__main__":
    main()