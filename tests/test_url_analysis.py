import sys
from pathlib import Path

from fastapi.testclient import TestClient


# Add the backend folder to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.main import app


client = TestClient(app)


def test_safe_google_url():
    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": "https://www.google.com"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["classification"] == "safe"
    assert data["risk_score"] < 40
    assert data["legitimate_probability"] > data["phishing_probability"]


def test_phishing_url():
    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": "http://secure-login-example.com/verify/account"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["classification"] == "phishing"
    assert data["risk_score"] >= 75
    assert data["phishing_probability"] > data["legitimate_probability"]


def test_ip_address_url():
    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": "http://192.168.1.100/login"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["classification"] == "phishing"
    assert data["risk_score"] >= 75

    messages = [
        indicator["message"]
        for indicator in data["indicators"]
    ]

    assert any(
        "IP address" in message
        for message in messages
    )


def test_at_symbol_url():
    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": "http://google.com@evil-example.com/login"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["classification"] == "phishing"
    assert data["risk_score"] >= 75

    messages = [
        indicator["message"]
        for indicator in data["indicators"]
    ]

    assert any(
        "@" in message
        for message in messages
    )


def test_long_url():
    long_path = "a" * 120

    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": f"https://example.com/{long_path}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    messages = [
        indicator["message"]
        for indicator in data["indicators"]
    ]

    assert any(
        "unusually long" in message
        for message in messages
    )


def test_many_subdomains():
    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": "https://a.b.c.example.com/login"
        },
    )

    assert response.status_code == 200

    data = response.json()

    messages = [
        indicator["message"]
        for indicator in data["indicators"]
    ]

    assert any(
        "number of subdomains" in message
        for message in messages
    )


def test_suspicious_keywords():
    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": (
                "https://example.com/"
                "login/verify/account/password"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    messages = [
        indicator["message"]
        for indicator in data["indicators"]
    ]

    assert any(
        "security-sensitive keywords" in message
        for message in messages
    )


def test_invalid_url():
    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": "not-a-valid-url"
        },
    )

    assert response.status_code == 422


def test_trailing_slash_consistency():
    response_without_slash = client.post(
        "/api/v1/analyze/url",
        json={
            "url": "https://www.google.com"
        },
    )

    response_with_slash = client.post(
        "/api/v1/analyze/url",
        json={
            "url": "https://www.google.com/"
        },
    )

    assert response_without_slash.status_code == 200
    assert response_with_slash.status_code == 200

    data_without_slash = response_without_slash.json()
    data_with_slash = response_with_slash.json()

    assert (
        data_without_slash["classification"]
        == data_with_slash["classification"]
    )

    assert (
        data_without_slash["risk_score"]
        == data_with_slash["risk_score"]
    )

    assert (
        data_without_slash["phishing_probability"]
        == data_with_slash["phishing_probability"]
    )

    assert (
        data_without_slash["legitimate_probability"]
        == data_with_slash["legitimate_probability"]
    )


def test_response_structure():
    response = client.post(
        "/api/v1/analyze/url",
        json={"url": "https://www.google.com/"},
    )

    assert response.status_code == 200

    data = response.json()

    expected_keys = {
        "url",
        "classification",
        "risk_score",
        "phishing_probability",
        "legitimate_probability",
        "indicators",
        "signals",
    }

    assert set(data.keys()) == expected_keys

    assert isinstance(data["url"], str)
    assert isinstance(data["classification"], str)
    assert isinstance(data["risk_score"], int)
    assert isinstance(data["phishing_probability"], float)
    assert isinstance(data["legitimate_probability"], float)
    assert isinstance(data["indicators"], list)
    assert isinstance(data["signals"], list)