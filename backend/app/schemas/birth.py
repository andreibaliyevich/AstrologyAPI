from datetime import datetime
from typing import Annotated
from pydantic import AfterValidator, BaseModel
from app.validators.time_zone import validate_time_zone


class BirthInfo(BaseModel):
    date_time: datetime
    time_zone: Annotated[str, AfterValidator(validate_time_zone)]
    latitude: float
    longitude: float
