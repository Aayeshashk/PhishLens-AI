def calculate_risk(
    phishing_probability: float,
    features: dict,
) -> dict:
    """
    Calculate a bounded PhishLens risk score.

    The ML phishing probability is the primary signal.
    Security indicators provide a controlled adjustment.

    Final classification:
        0-39   -> safe
        40-74  -> suspicious
        75-100 -> phishing
    """

    # Keep the ML probability within a valid range.
    phishing_probability = max(
        0.0,
        min(float(phishing_probability), 1.0),
    )

    # Start with the ML probability as the main risk signal.
    risk = phishing_probability * 100

    indicators = []
    rule_adjustment = 0

    # ---------------------------------------------------------
    # HTTPS
    # ---------------------------------------------------------

    if features["has_https"] == 0:
        indicators.append(
            {
                "type": "warning",
                "severity": "medium",
                "message": "URL does not use HTTPS.",
            }
        )

        rule_adjustment += 5

    # ---------------------------------------------------------
    # IP address
    # ---------------------------------------------------------

    if features["has_ip_address"] == 1:
        indicators.append(
            {
                "type": "warning",
                "severity": "high",
                "message": (
                    "URL uses an IP address instead of "
                    "a domain name."
                ),
            }
        )

        rule_adjustment += 12

    # ---------------------------------------------------------
    # @ symbol
    # ---------------------------------------------------------

    if features["has_at_symbol"] == 1:
        indicators.append(
            {
                "type": "warning",
                "severity": "high",
                "message": (
                    "URL contains an '@' symbol, which can "
                    "be used to obscure the actual destination."
                ),
            }
        )

        rule_adjustment += 12

    # ---------------------------------------------------------
    # Unusually long URL
    # ---------------------------------------------------------

    if features["url_length"] > 100:
        indicators.append(
            {
                "type": "warning",
                "severity": "medium",
                "message": "URL is unusually long.",
            }
        )

        rule_adjustment += 5

    # ---------------------------------------------------------
    # Many subdomains
    # ---------------------------------------------------------

    if features["subdomain_count"] >= 3:
        indicators.append(
            {
                "type": "warning",
                "severity": "medium",
                "message": (
                    "URL contains an unusually high "
                    "number of subdomains."
                ),
            }
        )

        rule_adjustment += 5

    # ---------------------------------------------------------
    # Suspicious keywords
    # ---------------------------------------------------------

    keyword_count = features[
        "suspicious_keyword_count"
    ]

    if keyword_count >= 2:
        indicators.append(
            {
                "type": "warning",
                "severity": "medium",
                "message": (
                    f"URL contains {keyword_count} "
                    "security-sensitive keywords."
                ),
            }
        )

        # Cap keyword contribution so that multiple
        # keywords cannot dominate the ML probability.
        rule_adjustment += min(
            keyword_count * 2,
            8,
        )

    # ---------------------------------------------------------
    # Special-character pattern
    # ---------------------------------------------------------

    if features["at_count"] > 0:
        indicators.append(
            {
                "type": "warning",
                "severity": "medium",
                "message": (
                    "URL contains special-character patterns "
                    "that may obscure its destination."
                ),
            }
        )

        # Avoid double-counting the @ symbol heavily.
        rule_adjustment += 2

    # ---------------------------------------------------------
    # Apply bounded rule adjustment
    # ---------------------------------------------------------

    # Security rules can add at most 35 points.
    rule_adjustment = min(
        rule_adjustment,
        35,
    )

    risk = risk + rule_adjustment

    # Always keep the final score in 0-100.
    risk = max(
        0,
        min(round(risk), 100),
    )

    # ---------------------------------------------------------
    # Final classification
    # ---------------------------------------------------------

    if risk >= 75:
        classification = "phishing"
    elif risk >= 40:
        classification = "suspicious"
    else:
        classification = "safe"

    return {
        "risk_score": risk,
        "classification": classification,
        "indicators": indicators,
    }