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
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
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
