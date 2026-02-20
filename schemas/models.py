from pydantic import BaseModel
from typing import Literal


class IntakeOutput(BaseModel):
    category: Literal["analysis", "generation", "validation", "unknown"]
    reasoning: str


class ExecutionOutput(BaseModel):
    result: str
    reasoning: str
    confidence: float


class ValidationOutput(BaseModel):
    approved: bool
    feedback: str
