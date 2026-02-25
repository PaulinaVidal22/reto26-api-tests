from pydantic import BaseModel
from typing import Dict, Any, Optional


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = {}


class ErrorResponse(BaseModel):
    error: ErrorDetail