from app.schemas.birth import BirthInfo
from app.schemas.compatibility import CompatibilityCharts
from app.utils.natal_chart import build_natal_chart
from app.utils.compatibility import compare_charts


class ChartService:
    async def build_chart(self, data: BirthInfo):
        return build_natal_chart(
            date_time=data.date_time,
            latitude=data.latitude,
            longitude=data.longitude,
            time_zone=data.time_zone,
        )

    async def compare_charts(self, data: CompatibilityCharts):
        return compare_charts(chart1=data.chart1, chart2=data.chart2)
