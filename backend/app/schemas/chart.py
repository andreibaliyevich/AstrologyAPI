from pydantic import BaseModel, Field
from app.schemas.aspect import Aspect
from app.schemas.planet import PlanetPosition


class NatalChart(BaseModel):
    ascendant: float
    midheaven: float
    planets: dict[str, PlanetPosition] = Field(default_factory=dict)
    houses: list[float] = Field(default_factory=list)
    aspects: list[Aspect] = Field(default_factory=list)
