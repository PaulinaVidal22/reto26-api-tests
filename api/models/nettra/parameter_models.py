from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class ParameterMeasurement(BaseModel):
    id: UUID
    well_id: UUID
    parameter_type_id: UUID
    t_from: datetime
    t_to: datetime
    avg_value: Optional[float]
    std_dev: Optional[float]


class ParameterResponse(BaseModel):
    page: int
    page_size: int
    data: list[ParameterMeasurement]