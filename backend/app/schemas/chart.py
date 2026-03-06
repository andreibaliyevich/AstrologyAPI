from pydantic import BaseModel, Field
from app.schemas.aspect import Aspect
from app.schemas.planet import PlanetPosition


class NatalChart(BaseModel):
    ascendant: float
    midheaven: float

    house1: float
    house2: float
    house3: float
    house4: float
    house5: float
    house6: float
    house7: float
    house8: float
    house9: float
    house10: float
    house11: float
    house12: float

    planets: list[PlanetPosition] = Field(default_factory=list)
    aspects: list[Aspect] = Field(default_factory=list)
