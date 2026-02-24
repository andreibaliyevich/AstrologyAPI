"""
Low-level mathematical and astronomical helper functions.

This module contains pure utility functions used for astrological
calculations, including:

- Angle normalization
- Zodiac sign detection
- Angular distance calculation
- House determination
- Julian Day conversion

These functions do not depend on business logic and can be reused
independently of natal chart or compatibility calculations.
"""

from datetime import datetime, timezone
import swisseph as swe
from app.constants import ZODIAC_SIGNS


def normalize_angle(angle: float) -> float:
    """
    Normalize an angle to the 0-360 degree range.

    :param angle: Angle in degrees.
    :type angle: float

    :returns: Normalized angle.
    :rtype: float
    """
    return angle % 360


def get_sign(longitude: float) -> tuple[str, float]:
    """
    Determine zodiac sign and degree within sign from longitude.

    :param longitude: Ecliptic longitude (0-360 degrees).
    :type longitude: float

    :returns: Tuple of (sign name, degree in sign).
    :rtype: tuple[str, float]
    """
    sign_index = int(longitude // 30)
    degree = longitude % 30
    return ZODIAC_SIGNS[sign_index], degree


def angle_difference(a: float, b: float) -> float:
    """
    Calculate the minimal angular distance between two positions.

    :param a: First angle in degrees.
    :type a: float

    :param b: Second angle in degrees.
    :type b: float

    :returns: Minimal angular difference (0-180).
    :rtype: float
    """
    diff = abs(a - b)
    return min(diff, 360 - diff)


def determine_house(longitude: float, houses: list[float]) -> int | None:
    """
    Determine the astrological house for a given longitude.

    :param longitude: Planet longitude.
    :type longitude: float

    :param houses: List of 12 house cusp longitudes.
    :type houses: list[float]

    :returns: House number (1-12) or None if not determined.
    :rtype: int | None
    """
    for i in range(12):
        start = houses[i]
        end = houses[(i + 1) % 12]

        if start < end:
            if start <= longitude < end:
                return i + 1
        else:
            if longitude >= start or longitude < end:
                return i + 1
    return None


def calculate_julian_day(dt: datetime) -> float:
    """
    Convert a timezone-aware datetime into Julian Day (UT).

    The datetime is converted to UTC before calculating Julian Day.

    :param dt: Timezone-aware datetime.
    :type dt: datetime

    :returns: Julian Day number in Universal Time.
    :rtype: float

    :raises ValueError: If datetime is not timezone-aware.
    """
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    dt_utc = dt.astimezone(timezone.utc)
    return swe.julday(
        dt_utc.year,
        dt_utc.month,
        dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600
    )
