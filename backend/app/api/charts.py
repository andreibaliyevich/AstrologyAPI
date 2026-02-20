from typing import Annotated
from fastapi import APIRouter, Body
from app.schemas.birth import BirthInfo
from app.schemas.chart import NatalChart
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
