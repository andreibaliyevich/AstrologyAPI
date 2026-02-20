from pydantic import BaseModel, Field
from app.schemas.chart import NatalChart


class CompatibilityCharts(BaseModel):
    chart1: NatalChart
    chart2: NatalChart


class CompatibilityInfo(BaseModel):
    total_score: float
    blocks: dict[str, float] = Field(default_factory=dict)
    aspect_count: int
