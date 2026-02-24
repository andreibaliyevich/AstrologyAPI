from datetime import datetime
from pydantic import BaseModel


class BirthInfo(BaseModel):
    date_time: datetime
    latitude: float
    longitude: float
    tz_offset_hours: float
