from fastapi import APIRouter

from app.models.request_models import RmdRequest
from app.services.rmd_engine import calculate_schedule

router = APIRouter()


@router.post("/calculate")
def calculate_rmd(request: RmdRequest):

    result = calculate_schedule(request.dict())

    return result