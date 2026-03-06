import swisseph as swe


EPHE_FOLDER = "./ephe"  # Path to the folder with ephemeris
HOUSE_SYSTEM = b'P'   # Placidus

ORBIS = {
    "conjunction": 8,
    "opposition": 8,
    "trine": 7,
    "square": 6,
    "sextile": 5,
}

ASPECT_ANGLES = {
    "conjunction": 0,
    "sextile": 60,
    "square": 90,
    "trine": 120,
    "opposition": 180,
}

PLANETS = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
    "uranus": swe.URANUS,
    "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO,
}

ZODIAC_SIGNS = [
    "aries", "taurus", "gemini", "cancer",
    "leo", "virgo", "libra", "scorpio",
    "sagittarius", "capricorn", "aquarius", "pisces",
]

HARMONIOUS = {"trine", "sextile"}
CHALLENGING = {"square", "opposition"}
NEUTRAL = {"conjunction"}

BLOCK_WEIGHTS = {
    "romantic": 0.30,
    "emotional": 0.25,
    "mental": 0.15,
    "sexual": 0.15,
    "stability": 0.15,
}
