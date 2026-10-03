import sys
from pathlib import Path


# Add the project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from ml.services.risk_engine import calculate_risk


def test_low_risk_url():
    features = {
        "has_https": 1,
        "has_ip_address": 0,
        "has_at_symbol": 0,
        "url_length": 20,
        "subdomain_count": 0,
        "suspicious_keyword_count": 0,
        "at_count": 0,
    }

    result = calculate_risk(
        phishing_probability=0.01,
        features=features,
    )

    assert result["classification"] == "safe"
    assert result["risk_score"] < 40
    assert result["indicators"] == []


def test_http_url_adds_risk():
    features = {
        "has_https": 0,
        "has_ip_address": 0,
        "has_at_symbol": 0,
        "url_length": 20,
        "subdomain_count": 0,
        "suspicious_keyword_count": 0,
        "at_count": 0,
    }

    result = calculate_risk(
        phishing_probability=0.01,
        features=features,
    )

    assert result["risk_score"] > 1

    messages = [
        indicator["message"]
        for indicator in result["indicators"]
    ]

    assert any(
        "HTTPS" in message
        for message in messages
    )


def test_ip_address_adds_high_risk():
    features = {
        "has_https": 1,
        "has_ip_address": 1,
        "has_at_symbol": 0,
        "url_length": 30,
        "subdomain_count": 0,
        "suspicious_keyword_count": 0,
        "at_count": 0,
    }

    result = calculate_risk(
        phishing_probability=0.50,
        features=features,
    )

    messages = [
        indicator["message"]
        for indicator in result["indicators"]
    ]

    assert any(
        "IP address" in message
        for message in messages
    )


def test_at_symbol_adds_indicator():
    features = {
        "has_https": 1,
        "has_ip_address": 0,
        "has_at_symbol": 1,
        "url_length": 30,
        "subdomain_count": 0,
        "suspicious_keyword_count": 0,
        "at_count": 1,
    }

    result = calculate_risk(
        phishing_probability=0.20,
        features=features,
    )

    messages = [
        indicator["message"]
        for indicator in result["indicators"]
    ]

    assert any(
        "@" in message
        for message in messages
    )


def test_long_url_adds_indicator():
    features = {
        "has_https": 1,
        "has_ip_address": 0,
        "has_at_symbol": 0,
        "url_length": 150,
        "subdomain_count": 0,
        "suspicious_keyword_count": 0,
        "at_count": 0,
    }

    result = calculate_risk(
        phishing_probability=0.10,
        features=features,
    )

    messages = [
        indicator["message"]
        for indicator in result["indicators"]
    ]

    assert any(
        "unusually long" in message
        for message in messages
    )


def test_many_subdomains_add_indicator():
    features = {
        "has_https": 1,
        "has_ip_address": 0,
        "has_at_symbol": 0,
        "url_length": 40,
        "subdomain_count": 4,
        "suspicious_keyword_count": 0,
        "at_count": 0,
    }

    result = calculate_risk(
        phishing_probability=0.10,
        features=features,
    )

    messages = [
        indicator["message"]
        for indicator in result["indicators"]
    ]

    assert any(
        "number of subdomains" in message
        for message in messages
    )


def test_suspicious_keywords_add_indicator():
    features = {
        "has_https": 1,
        "has_ip_address": 0,
        "has_at_symbol": 0,
        "url_length": 40,
        "subdomain_count": 0,
        "suspicious_keyword_count": 3,
        "at_count": 0,
    }

    result = calculate_risk(
        phishing_probability=0.20,
        features=features,
    )

    messages = [
        indicator["message"]
        for indicator in result["indicators"]
    ]

    assert any(
        "security-sensitive keywords" in message
        for message in messages
    )


def test_risk_score_is_capped_at_100():
    features = {
        "has_https": 0,
        "has_ip_address": 1,
        "has_at_symbol": 1,
        "url_length": 150,
        "subdomain_count": 5,
        "suspicious_keyword_count": 5,
        "at_count": 1,
    }

    result = calculate_risk(
        phishing_probability=1.0,
        features=features,
    )

    assert result["risk_score"] == 100
    assert result["classification"] == "phishing"