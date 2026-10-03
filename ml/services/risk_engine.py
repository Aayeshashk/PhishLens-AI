def calculate_risk(
    phishing_probability: float,
    features: dict,
) -> dict:

    risk = phishing_probability * 100

    indicators = []

    # HTTPS check
    if features["has_https"] == 0:
        indicators.append({
            "type": "warning",
            "severity": "medium",
            "message": "URL does not use HTTPS.",
        })

        risk += 8

    # IP address check
    if features["has_ip_address"] == 1:
        indicators.append({
            "type": "warning",
            "severity": "high",
            "message": (
                "URL uses an IP address instead of "
                "a domain name."
            ),
        })

        risk += 15

    # @ symbol check
    if features["has_at_symbol"] == 1:
        indicators.append({
            "type": "warning",
            "severity": "high",
            "message": (
                "URL contains an '@' symbol, which can "
                "be used to obscure the actual destination."
            ),
        })

        risk += 15

    # Long URL check
    if features["url_length"] > 100:
        indicators.append({
            "type": "warning",
            "severity": "medium",
            "message": "URL is unusually long.",
        })

        risk += 8

    # Subdomain check
    if features["subdomain_count"] >= 3:
        indicators.append({
            "type": "warning",
            "severity": "medium",
            "message": (
                "URL contains an unusually high "
                "number of subdomains."
            ),
        })

        risk += 8

    # Suspicious keyword check
    keyword_count = features["suspicious_keyword_count"]

    if keyword_count >= 2:
        indicators.append({
            "type": "warning",
            "severity": "medium",
            "message": (
                f"URL contains {keyword_count} "
                "security-sensitive keywords."
            ),
        })

        risk += min(keyword_count * 3, 12)

    # Special-character pattern
    if features["at_count"] > 0:
        indicators.append({
            "type": "warning",
            "severity": "medium",
            "message": (
                "URL contains special-character patterns "
                "that may obscure its destination."
            ),
        })

    # Keep risk score between 0 and 100
    risk = max(0, min(round(risk), 100))

    # Final classification
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