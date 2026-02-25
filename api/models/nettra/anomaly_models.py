from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID


class Anomaly(BaseModel):
    id: UUID
    anomaly_code: str
    anomaly_name: str
    t_from: datetime
    t_to: datetime


class Pagination(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    total: int = Field(ge=0)


class AnomaliesResponse(BaseModel):
    data: List[Anomaly]
    pagination: Pagination