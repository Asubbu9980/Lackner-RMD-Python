from pydantic import BaseModel
from typing import List, Optional


class ScheduleRow(BaseModel):
    yr: int
    year: int
    age: int
    factor: Optional[float]
    beginBalance: float
    rmd: float
    tax: float
    net: float
    growth: float
    endBalance: float
    cumRmd: float
    cumTax: float
    cumGrowth: float


class RmdResponse(BaseModel):
    balanceStart: float
    totalRmd: float
    totalTax: float
    totalGrowth: float
    endingBalance: float
    rows: List[ScheduleRow]