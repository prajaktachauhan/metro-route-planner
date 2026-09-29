"""Distance, time and fare calculations."""

from .config import AVERAGE_SPEED_KMPH, FARE_SLABS, MAX_FARE
from .models import Journey


def calculate_distance(route, metro):
    """Sum the edge distances along a route.

    Raises ValueError if two consecutive stations are not directly connected.
    """
    total = 0
    for current, nxt in zip(route, route[1:]):
        try:
            total += metro[current][nxt]
        except KeyError:
            raise ValueError(f"{current} and {nxt} are not directly connected.")
    return total


def calculate_time(distance, speed=AVERAGE_SPEED_KMPH):
    """Estimated travel time in minutes at the given average speed."""
    if distance < 0:
        raise ValueError("Distance cannot be negative.")
    if speed <= 0:
        raise ValueError("Speed must be positive.")
    return round(distance / speed * 60, 2)


def calculate_fare(distance):
    """Fare based on distance slabs defined in config.FARE_SLABS."""
    if distance < 0:
        raise ValueError("Distance cannot be negative.")
    for limit, fare in FARE_SLABS:
        if distance <= limit:
            return fare
    return MAX_FARE


def build_journey(route, metro):
    """Compute all metrics for a route and return a Journey object."""
    distance = calculate_distance(route, metro)
    return Journey(
        route=tuple(route),
        distance=distance,
        time_minutes=calculate_time(distance),
        fare=calculate_fare(distance),
    )
