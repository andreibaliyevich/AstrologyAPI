from app.schemas.birth import BirthInfo
from app.utils.natal_chart import build_natal_chart


class ChartService:
    async def build_chart(self, data: BirthInfo):
        return build_natal_chart(
            dt=data.date_time,
            latitude=data.latitude,
            longitude=data.longitude,
            tz_offset_hours=data.tz_offset_hours,
        )
