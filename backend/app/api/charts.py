from typing import Annotated
from fastapi import APIRouter, Body
from app.schemas.birth import BirthInfo
from app.schemas.chart import NatalChart
from app.schemas.compatibility import CompatibilityCharts, CompatibilityInfo
from app.services.chart import ChartService


router = APIRouter(
    prefix="/charts",
    tags=["Charts"],
)


@router.post("/build", response_model=NatalChart)
async def chart_build(
    body_data: Annotated[BirthInfo, Body()],
) -> NatalChart:
    service = ChartService()
    return await service.build_chart(data=body_data)


@router.post("/compare", response_model=CompatibilityInfo)
async def charts_compare(
    body_data: Annotated[CompatibilityCharts, Body()],
) -> CompatibilityInfo:
    service = ChartService()
    return await service.compare_charts(data=body_data)
