"""
Natal chart calculation module.

This module provides functionality for building a full natal chart
based on birth date, time, and location.

It includes:

- Planetary position calculations
- House cusp calculations (Placidus system)
- House assignment
- Aspect detection within a single chart
- Main entry function for chart construction
"""

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import swisseph as swe
from app.schemas.aspect import Aspect
from app.schemas.chart import NatalChart
from app.schemas.planet import PlanetPosition
from app.utils.astro_math import (
    normalize_angle,
    get_sign,
    angle_difference,
    determine_house,
    calculate_julian_day,
)
from app.constants import (
    EPHE_FOLDER,
    HOUSE_SYSTEM,
    ORBIS,
    ASPECT_ANGLES,
    PLANETS,
)


def calculate_planets(jd: float) -> list[PlanetPosition]:
    """
    Calculate planetary longitudes for a given Julian Day.

    :param jd: Julian Day in Universal Time.
    :type jd: float

    :returns: List of planetary positions.
    :rtype: list[PlanetPosition]
    """
    planets: list[PlanetPosition] = []

    for name, code in PLANETS.items():
        pos = swe.calc_ut(jd, code)[0]
        longitude = normalize_angle(pos[0])

        speed = pos[3]
        is_retrograde = speed < 0

        sign, degree = get_sign(longitude)

        planets.append(PlanetPosition(
            name=name,
            longitude=longitude,
            sign=sign,
            degree_in_sign=degree,
            is_retrograde=is_retrograde,
            house=None,
        ))

    return planets


def calculate_houses(
    jd: float,
    lat: float,
    lon: float,
) -> tuple[list[float], float, float]:
    """
    Calculate house cusps, ascendant and midheaven using Placidus system.

    :param jd: Julian Day in Universal Time.
    :type jd: float

    :param lat: Geographic latitude.
    :type lat: float

    :param lon: Geographic longitude.
    :type lon: float

    :returns: Tuple containing:
              - Ascendant longitude
              - Midheaven longitude
              - List of 12 house cusp longitudes
    :rtype: tuple[list[float], float, float]
    """
    houses, ascmc = swe.houses(jd, lat, lon, HOUSE_SYSTEM)

    houses = [normalize_angle(h) for h in houses]
    ascendant = normalize_angle(ascmc[0])
    midheaven = normalize_angle(ascmc[1])

    return houses, ascendant, midheaven


def assign_houses(planets: list[PlanetPosition], houses: list[float]) -> None:
    """
    Assign house numbers to planetary positions.

    :param planets: List of planetary positions.
    :type planets: list[PlanetPosition]

    :param houses: List of house cusp longitudes.
    :type houses: list[float]
    """
    for planet in planets:
        planet.house = determine_house(planet.longitude, houses)


def calculate_aspects(planets: list[PlanetPosition]) -> list[Aspect]:
    """
    Detect aspects between planets within a single natal chart.

    Aspects are determined based on predefined aspect angles
    and allowed orb values.

    :param planets: List of planetary positions.
    :type planets: list[PlanetPosition]

    :returns: List of detected aspects.
    :rtype: list[Aspect]
    """
    aspects: list[Aspect] = []

    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            p1 = planets[i]
            p2 = planets[j]

            diff = angle_difference(p1.longitude, p2.longitude)

            for aspect_name, angle in ASPECT_ANGLES.items():
                orb = abs(diff - angle)

                if orb <= ORBIS[aspect_name]:
                    aspects.append(Aspect(
                        planet1=p1.name,
                        planet2=p2.name,
                        aspect_type=aspect_name,
                        orb=round(orb, 2),
                    ))

    return aspects


def build_natal_chart(
    date_time: datetime,
    time_zone: str,
    latitude: float,
    longitude: float,
) -> NatalChart:
    """
    Build a natal chart based on birth data.

    This function calculates planetary positions, house cusps,
    ascendant, and aspects for a given birth moment and location.

    :param date_time: Local birth date and time (naive or timezone-aware).
    :type date_time: datetime

    :param time_zone: IANA timezone name (e.g. "Europe/London").
    :type time_zone: str

    :param latitude: Geographic latitude of birth location.
    :type latitude: float

    :param longitude: Geographic longitude of birth location.
    :type longitude: float

    :returns: Fully calculated natal chart model.
    :rtype: NatalChart
    """
    ephe_path = Path(EPHE_FOLDER)

    if ephe_path.is_dir():
        swe.set_ephe_path(EPHE_FOLDER)

    tz = ZoneInfo(time_zone)

    if date_time.tzinfo is None:
        date_time = date_time.replace(tzinfo=tz)
    else:
        date_time = date_time.astimezone(tz)

    jd = calculate_julian_day(date_time)

    planets = calculate_planets(jd)
    houses, ascendant, midheaven = calculate_houses(jd, latitude, longitude)

    assign_houses(planets, houses)
    aspects = calculate_aspects(planets)

    return NatalChart(
        ascendant=ascendant,
        midheaven=midheaven,
        house1=houses[0],
        house2=houses[1],
        house3=houses[2],
        house4=houses[3],
        house5=houses[4],
        house6=houses[5],
        house7=houses[6],
        house8=houses[7],
        house9=houses[8],
        house10=houses[9],
        house11=houses[10],
        house12=houses[11],
        planets=planets,
        aspects=aspects,
    )
