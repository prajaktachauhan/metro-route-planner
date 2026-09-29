"""Validated user input.

Every function accepts `input_fn` and `output_fn` so tests can feed scripted
answers instead of using the real keyboard.
"""

import logging

from .config import CRITERION_DISTANCE, CRITERION_STOPS
from .graph import normalize_station

logger = logging.getLogger(__name__)


def read_station(prompt, metro, input_fn=input, output_fn=print, exclude=None):
    """Ask for a station until a valid one is entered (case-insensitive).

    `exclude` rejects one particular station (e.g. destination == start).
    """
    while True:
        station = normalize_station(input_fn(prompt), metro)
        if station is None:
            output_fn("Invalid station name. Please try again.")
            logger.warning("Invalid station entered")
        elif station == exclude:
            output_fn(f"Please choose a station other than {exclude}.")
        else:
            return station


def ask_yes_no(prompt, input_fn=input, output_fn=print):
    """Return True for yes/y and False for no/n; re-ask on anything else."""
    while True:
        answer = input_fn(prompt).strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        output_fn("Please answer 'yes' or 'no'.")


def read_criterion(input_fn=input, output_fn=print):
    """Let the user choose between shortest distance and fewest stations."""
    output_fn("\nChoose route type:")
    output_fn("  1. Shortest distance (default)")
    output_fn("  2. Fewest stations")
    while True:
        choice = input_fn("Enter 1 or 2: ").strip()
        if choice in ("", "1"):
            return CRITERION_DISTANCE
        if choice == "2":
            return CRITERION_STOPS
        output_fn("Invalid choice. Please enter 1 or 2.")


def read_closed_stations(metro, start, destination,
                         input_fn=input, output_fn=print):
    """Ask for one or more closed stations (comma-separated).

    Rejects unknown names and the start/destination stations.
    """
    while True:
        raw = input_fn("Enter closed station(s), comma-separated: ")
        names = [n for n in raw.split(",") if n.strip()]
        if not names:
            output_fn("Please enter at least one station.")
            continue
        closed, problem = [], None
        for name in names:
            station = normalize_station(name, metro)
            if station is None:
                problem = f"Invalid station name: '{name.strip()}'."
                break
            if station in (start, destination):
                problem = (f"{station} is your start/destination and "
                           "cannot be closed for this trip.")
                break
            closed.append(station)
        if problem:
            output_fn(problem + " Please try again.")
            continue
        logger.info("Closed stations chosen: %s", closed)
        return set(closed)
