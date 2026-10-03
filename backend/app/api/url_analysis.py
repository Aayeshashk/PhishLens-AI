from fastapi import APIRouter

from app.schemas.url_analysis import (
    URLAnalysisRequest,
    URLAnalysisResponse,
)

from app.services.url_analysis_service import analyze_url


router = APIRouter(
    prefix="/api/v1/analyze",
    tags=["URL Analysis"],
)


@router.post(
    "/url",
    response_model=URLAnalysisResponse,
)
def analyze_url_endpoint(
    request: URLAnalysisRequest,
):
    return analyze_url(str(request.url))