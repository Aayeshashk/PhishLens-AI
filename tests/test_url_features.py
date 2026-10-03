import sys
from pathlib import Path


# Add the project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from ml.features.url_features import extract_url_features


def test_basic_url_features():
    features = extract_url_features(
        "https://www.google.com"
    )

    assert features["has_https"] == 1
    assert features["has_ip_address"] == 0
    assert features["has_at_symbol"] == 0
    assert features["subdomain_count"] == 1


def test_http_detection():
    features = extract_url_features(
        "http://example.com"
    )

    assert features["has_https"] == 0


def test_ip_address_detection():
    features = extract_url_features(
        "http://192.168.1.100/login"
    )

    assert features["has_ip_address"] == 1


def test_at_symbol_detection():
    features = extract_url_features(
        "http://google.com@evil-example.com/login"
    )

    assert features["has_at_symbol"] == 1
    assert features["at_count"] == 1


def test_subdomain_count():
    features = extract_url_features(
        "https://a.b.c.example.com/login"
    )

    assert features["subdomain_count"] == 3


def test_suspicious_keywords():
    features = extract_url_features(
        "https://example.com/login/verify/account"
    )

    assert features["keyword_login"] == 1
    assert features["keyword_verify"] == 1
    assert features["keyword_account"] == 1

    assert features["suspicious_keyword_count"] == 3


def test_query_parameters():
    features = extract_url_features(
        "https://example.com/login?user=a&token=b"
    )

    assert features["query_parameter_count"] == 2
    assert features["question_mark_count"] == 1
    assert features["equal_count"] == 2
    assert features["ampersand_count"] == 1


def test_trailing_slash_normalization():
    features_without_slash = extract_url_features(
        "https://www.google.com"
    )

    features_with_slash = extract_url_features(
        "https://www.google.com/"
    )

    assert (
        features_without_slash
        == features_with_slash
    )


def test_feature_count():
    features = extract_url_features(
        "https://example.com/login"
    )

    assert len(features) == 34