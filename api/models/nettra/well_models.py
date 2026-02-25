from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class WellSummary(BaseModel):
    id: UUID
    name: str
    device_id: str


class WellsListResponse(BaseModel):
    items: List[WellSummary]
    page: int
    page_size: int
    total: int


class WellDetail(BaseModel):
    id: UUID
    name: str
    device_id: str
    category_id: UUID
    category_name: Optional[str]
    category_description: Optional[str]