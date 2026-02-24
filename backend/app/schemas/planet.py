from pydantic import BaseModel


class PlanetPosition(BaseModel):
    name: str
    longitude: float
    sign: str
    degree_in_sign: float
    is_retrograde: bool
    house: int | None
