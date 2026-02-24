from pydantic import BaseModel


class Aspect(BaseModel):
    planet1: str
    planet2: str
    aspect_type: str
    orb: float
