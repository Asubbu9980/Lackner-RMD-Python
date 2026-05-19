from fastapi import APIRouter

from app.models.request_models import RmdRequest
from app.services.rmd_engine import calculate_schedule

from app.services.charts import generate_chart_data
router = APIRouter()


@router.post("/calculate")
def calculate_rmd(request: RmdRequest):

    result = calculate_schedule(request.dict())

    return result


@router.post("/charts/{scenario}")
def get_chart_data(
    scenario: str,
    request: RmdRequest
):

    # Convert request to dictionary
    data = request.dict()

    # Override scenario from URL
    data["scenario"] = scenario

    # Calculate RMD schedule
    result = calculate_schedule(data)

    # Generate chart response
    chart_data = generate_chart_data(result["rows"])
    #print(chart_data)
    return {
        "scenario": scenario,
        "charts": chart_data
    }