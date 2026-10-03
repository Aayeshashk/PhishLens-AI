from pydantic import BaseModel, HttpUrl


class URLAnalysisRequest(BaseModel):
    url: HttpUrl


class SecurityIndicator(BaseModel):
    type: str
    severity: str
    message: str


class URLAnalysisResponse(BaseModel):
    url: str
    classification: str
    risk_score: int
    phishing_probability: float
    legitimate_probability: float
    indicators: list[SecurityIndicator]