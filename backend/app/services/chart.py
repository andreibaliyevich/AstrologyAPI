from app.schemas.birth import BirthInfo
from app.schemas.compatibility import CompatibilityCharts
from app.utils.natal_chart import build_natal_chart
from app.utils.compatibility import compare_charts


class ChartService:
    async def build_chart(self, data: BirthInfo):
        return build_natal_chart(
            dt=data.date_time,
            latitude=data.latitude,
            longitude=data.longitude,
            tz_offset_hours=data.tz_offset_hours,
        )

    async def compare_charts(self, data: CompatibilityCharts):
        return compare_charts(data.chart1, data.chart2)
