"""Formatting helpers: build text, let the caller decide where to print it."""

from .config import CURRENCY
from .graph import get_stations


def format_station_list(metro):
    lines = ["Available Stations:"]
    lines += [f"- {name}" for name in get_stations(metro)]
    return "\n".join(lines)


def format_route(route):
    """'A -> B -> C'"""
    return " -> ".join(route)


def format_journey(title, journey):
    """Full block of route and journey details."""
    return "\n".join([
        f"\n{title}",
        format_route(journey.route),
        "\nJOURNEY DETAILS",
        f"Distance: {journey.distance} km",
        f"Estimated Time: {journey.time_minutes} minutes",
        f"Estimated Cost: {CURRENCY} {journey.fare}",
        f"Number of Stations: {journey.stops}",
    ])


def format_comparison(original, alternate):
    """Show how much the detour costs the traveller."""
    def signed(value):
        return f"{value:+g}"
    return "\n".join([
        "\nCOMPARISON (alternate vs original)",
        f"Distance: {signed(alternate.distance - original.distance)} km",
        f"Time: {signed(round(alternate.time_minutes - original.time_minutes, 2))} minutes",
        f"Cost: {signed(alternate.fare - original.fare)} {CURRENCY}",
    ])
