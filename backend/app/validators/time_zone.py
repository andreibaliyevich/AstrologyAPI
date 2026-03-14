from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def validate_time_zone(value: str) -> str:
    try:
        ZoneInfo(value)
    except ZoneInfoNotFoundError:
        raise ValueError("Invalid timezone.")
    return value
