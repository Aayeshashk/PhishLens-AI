from ml.services.prediction_service import PhishLensPredictor


predictor = PhishLensPredictor()


def analyze_url(url: str) -> dict:
    return predictor.predict(url)