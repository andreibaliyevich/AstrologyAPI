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

from datetime import datetime, timedelta, timezone
from pathlib import Path
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


def calculate_planets(jd: float) -> dict[str, PlanetPosition]:
    """
    Calculate planetary longitudes for a given Julian Day.

    :param jd: Julian Day in Universal Time.
    :type jd: float

    :returns: Dictionary of planetary positions keyed by planet name.
    :rtype: dict[str, PlanetPosition]
    """
    planets = {}

    for name, code in PLANETS.items():
        pos = swe.calc_ut(jd, code)[0]
        longitude = normalize_angle(pos[0])

        speed = pos[3]
        is_retrograde = speed < 0

        sign, degree = get_sign(longitude)

        planets[name] = PlanetPosition(
            name=name,
            longitude=longitude,
            sign=sign,
            degree_in_sign=degree,
            is_retrograde=is_retrograde,
            house=None,
        )

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


def assign_houses(planets: dict[str, PlanetPosition], houses: list[float]) -> None:
    """
    Assign house numbers to planetary positions.

    :param planets: Dictionary of planetary positions.
    :type planets: dict[str, PlanetPosition]

    :param houses: List of house cusp longitudes.
    :type houses: list[float]
    """
    for planet in planets.values():
        planet.house = determine_house(planet.longitude, houses)


def calculate_aspects(planets: dict[str, PlanetPosition]) -> list[Aspect]:
    """
    Detect aspects between planets within a single natal chart.

    Aspects are determined based on predefined aspect angles
    and allowed orb values.

    :param planets: Dictionary of planetary positions.
    :type planets: dict[str, PlanetPosition]

    :returns: List of detected aspects.
    :rtype: list[Aspect]
    """
    aspects = []
    names = list(planets.keys())

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            p1 = planets[names[i]]
            p2 = planets[names[j]]

            diff = angle_difference(p1.longitude, p2.longitude)

            for aspect_name, angle in ASPECT_ANGLES.items():
                orb = abs(diff - angle)
                if orb <= ORBIS[aspect_name]:
                    aspects.append(
                        Aspect(
                            planet1=p1.name,
                            planet2=p2.name,
                            aspect_type=aspect_name,
                            orb=round(orb, 2),
                        )
                    )

    return aspects


def build_natal_chart(
    dt: datetime,
    latitude: float,
    longitude: float,
    tz_offset_hours: float,
) -> NatalChart:
    """
    Build a natal chart based on birth data.

    This function calculates planetary positions, house cusps,
    ascendant, and aspects for a given birth moment and location.

    :param dt: Local birth date and time (naive or timezone-aware).
    :type dt: datetime

    :param latitude: Geographic latitude of birth location.
    :type latitude: float

    :param longitude: Geographic longitude of birth location.
    :type longitude: float

    :param tz_offset_hours: Timezone offset from UTC in hours.
                            Example: +3 for UTC+3, -5 for UTC-5.
    :type tz_offset_hours: float

    :returns: Fully calculated natal chart model.
    :rtype: NatalChart
    """
    ephe_path = Path(EPHE_FOLDER)

    if ephe_path.is_dir():
        swe.set_ephe_path(EPHE_FOLDER)

    tz = timezone(timedelta(hours=tz_offset_hours))

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    else:
        dt = dt.astimezone(tz)

    jd = calculate_julian_day(dt)

    planets = calculate_planets(jd)
    houses, ascendant, midheaven = calculate_houses(jd, latitude, longitude)

    assign_houses(planets, houses)
    aspects = calculate_aspects(planets)

    return NatalChart(
        ascendant=ascendant,
        midheaven=midheaven,
        planets=planets,
        houses=houses,
        aspects=aspects,
    )
