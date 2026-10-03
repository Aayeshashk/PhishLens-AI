import re
from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = [
    "login",
    "signin",
    "verify",
    "verification",
    "secure",
    "account",
    "update",
    "password",
    "bank",
    "confirm",
    "authenticate",
    "credential",
    "wallet",
    "payment",
]


def extract_url_features(url: str) -> dict:
    # Normalize harmless trailing slashes.
    # This makes:
    # https://www.google.com
    # and
    # https://www.google.com/
    # produce the same features.
    url = url.rstrip("/")

    parsed = urlparse(url)

    hostname = parsed.netloc
    path = parsed.path
    query = parsed.query

    features = {}

    # Basic URL properties
    features["url_length"] = len(url)
    features["hostname_length"] = len(hostname)
    features["path_length"] = len(path)

    # Character counts
    features["dot_count"] = url.count(".")
    features["hyphen_count"] = url.count("-")
    features["underscore_count"] = url.count("_")

    # Count path separators only.
    # The trailing root "/" is normalized away above.
    features["slash_count"] = path.count("/")

    features["question_mark_count"] = url.count("?")
    features["equal_count"] = url.count("=")
    features["at_count"] = url.count("@")
    features["ampersand_count"] = url.count("&")
    features["percent_count"] = url.count("%")

    # Digit information
    features["digit_count"] = sum(
        char.isdigit()
        for char in url
    )

    # HTTPS
    features["has_https"] = int(
        parsed.scheme.lower() == "https"
    )

    # IP address detection
    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    features["has_ip_address"] = int(
        bool(re.match(ip_pattern, hostname))
    )

    # Suspicious URL characters
    features["has_at_symbol"] = int(
        "@" in url
    )

    features["has_double_slash"] = int(
        "//" in path
    )

    # Subdomain count
    hostname_without_port = hostname.split(":")[0]

    if hostname_without_port:
        features["subdomain_count"] = max(
            0,
            len(hostname_without_port.split(".")) - 2
        )
    else:
        features["subdomain_count"] = 0

    # Query parameters
    features["query_parameter_count"] = (
        len(query.split("&"))
        if query
        else 0
    )

    # Suspicious keywords
    url_lower = url.lower()

    for keyword in SUSPICIOUS_KEYWORDS:
        features[f"keyword_{keyword}"] = int(
            keyword in url_lower
        )

    features["suspicious_keyword_count"] = sum(
        features[f"keyword_{keyword}"]
        for keyword in SUSPICIOUS_KEYWORDS
    )

    return features