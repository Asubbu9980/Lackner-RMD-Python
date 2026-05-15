from pydantic import BaseModel
from typing import Optional

class RmdRequest(BaseModel):
    balance_Start: float
    growth_Rate: float
    tax_Rate: float
    year_Birth_Owner: int
    year_Birth_Beny: int
    date_Death_Owner: Optional[str] = None
    plan: str
    scenario: str