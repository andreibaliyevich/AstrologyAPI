"""
Synastry and compatibility calculation module.

This module provides functionality for comparing two natal charts
and calculating relationship compatibility scores.

It includes:

- Aspect scoring
- Synastry aspect detection
- Block-based compatibility evaluation
- Final compatibility aggregation
"""

from app.schemas.chart import NatalChart
from app.schemas.compatibility import CompatibilityInfo
from app.utils.astro_math import angle_difference
from app.constants import (
    HARMONIOUS,
    CHALLENGING,
    NEUTRAL,
    BLOCK_WEIGHTS,
    ORBIS,
    ASPECT_ANGLES,
)


def aspect_score(
    aspect_type: str,
    orb: float,
    max_orb: float,
) -> float:
    """
    Calculate weighted score contribution for a single aspect.

    :param aspect_type: Type of aspect (e.g. trine, square).
    :type aspect_type: str

    :param orb: Actual deviation from exact aspect.
    :type orb: float

    :param max_orb: Maximum allowed orb for this aspect.
    :type max_orb: float

    :returns: Signed score contribution.
    :rtype: float
    """
    strength = 1 - (orb / max_orb)

    if aspect_type in HARMONIOUS:
        return 1.0 * strength
    elif aspect_type in CHALLENGING:
        return -0.8 * strength
    elif aspect_type in NEUTRAL:
        return 0.6 * strength
    return 0


def calculate_synastry_aspects(
    chart1: NatalChart,
    chart2: NatalChart,
) -> list[tuple]:
    """
    Detect aspects between planets of two natal charts (synastry).

    :param chart1: First natal chart.
    :type chart1: NatalChart

    :param chart2: Second natal chart.
    :type chart2: NatalChart

    :returns: List of synastry aspect tuples containing:
              (planet1, planet2, aspect_type, orb, max_orb)
    :rtype: list[tuple]
    """
    results = []

    for p1 in chart1.planets.values():
        for p2 in chart2.planets.values():

            diff = angle_difference(p1.longitude, p2.longitude)

            for aspect_name, angle in ASPECT_ANGLES.items():
                orb = abs(diff - angle)
                max_orb = ORBIS[aspect_name]

                if orb <= max_orb:
                    results.append(
                        (
                            p1.name,
                            p2.name,
                            aspect_name,
                            orb,
                            max_orb,
                        )
                    )
    return results


def evaluate_block(block_aspects):
    """
    Calculate normalized score for a compatibility block.

    :param block_aspects: List of synastry aspects for a block.
    :type block_aspects: list[tuple]

    :returns: Normalized score in range 0–1.
    :rtype: float
    """
    total = 0
    for (_, _, aspect_type, orb, max_orb) in block_aspects:
        total += aspect_score(aspect_type, orb, max_orb)

    if block_aspects:
        normalized = (total + len(block_aspects)) / (2 * len(block_aspects))
    else:
        normalized = 0.5

    return max(0, min(1, normalized))


def compare_charts(
    chart1: NatalChart,
    chart2: NatalChart,
) -> CompatibilityInfo:
    """
    Compare two natal charts and calculate compatibility score.

    This function performs synastry analysis by detecting inter-chart aspects
    and evaluating compatibility across weighted relationship blocks:

    - Romantic
    - Emotional
    - Mental
    - Sexual
    - Stability

    :param chart1: First natal chart.
    :type chart1: NatalChart

    :param chart2: Second natal chart.
    :type chart2: NatalChart

    :returns: Compatibility result including total score and block scores.
    :rtype: CompatibilityInfo
    """
    aspects = calculate_synastry_aspects(chart1, chart2)

    blocks = {
        "romantic": [],
        "emotional": [],
        "mental": [],
        "sexual": [],
        "stability": [],
    }

    for a in aspects:
        p1, p2 = a[0], a[1]

        pair = {p1, p2}

        if pair <= {"Venus", "Mars"} or pair == {"Venus"}:
            blocks["romantic"].append(a)

        if pair <= {"Moon", "Sun"} or pair == {"Moon"}:
            blocks["emotional"].append(a)

        if pair <= {"Mercury", "Sun"} or pair == {"Mercury"}:
            blocks["mental"].append(a)

        if pair <= {"Mars", "Venus"} or pair == {"Mars"}:
            blocks["sexual"].append(a)

        if "Saturn" in pair:
            blocks["stability"].append(a)

    scores = {}
    total_score = 0

    for block_name, block_aspects in blocks.items():
        block_score = evaluate_block(block_aspects)
        scores[block_name] = round(block_score * 100, 1)
        total_score += block_score * BLOCK_WEIGHTS[block_name]

    final_score = round(total_score * 100, 1)

    return CompatibilityInfo(
        total_score=final_score,
        blocks=scores,
        aspect_count=len(aspects),
    )
