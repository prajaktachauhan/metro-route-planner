"""Orchestrates the complete user workflow."""

import logging

from .calculator import build_journey
from .config import CRITERION_DISTANCE
from .display import (format_comparison, format_journey,
                      format_station_list)
from .exceptions import NoRouteError
from .graph import validate_network
from .input_handler import (ask_yes_no, read_closed_stations,
                            read_criterion, read_station)
from .metro_data import METRO
from .route_finder import find_route

logger = logging.getLogger(__name__)


def plan_journey(metro, start, destination, closed_stations=None,
                 criterion=CRITERION_DISTANCE):
    """Find a route and compute its metrics. Raises MetroError subclasses."""
    route = find_route(metro, start, destination, closed_stations, criterion)
    return build_journey(route, metro)


def run_cli(metro=METRO, input_fn=input, output_fn=print):
    """Run the interactive planner. Returns the list of journeys planned."""
    validate_network(metro)
    logger.info("Session started")
    journeys = []

    output_fn("EFFICIENT METRO ROUTE PLANNER\n")
    output_fn(format_station_list(metro))

    start = read_station("\nEnter starting station: ", metro, input_fn, output_fn)
    destination = read_station("Enter destination station: ", metro,
                               input_fn, output_fn, exclude=start)
    criterion = read_criterion(input_fn, output_fn)

    try:
        journey = plan_journey(metro, start, destination, criterion=criterion)
    except NoRouteError:
        output_fn("\nNo route found.")
        logger.warning("No route %s -> %s", start, destination)
        output_fn("\nThank you for using Metro Route Planner!!")
        return journeys
    journeys.append(journey)
    output_fn(format_journey("RECOMMENDED ROUTE", journey))

    if ask_yes_no("\nIs any station closed? (yes/no): ", input_fn, output_fn):
        closed = read_closed_stations(metro, start, destination,
                                      input_fn, output_fn)
        try:
            alternate = plan_journey(metro, start, destination,
                                     closed, criterion)
        except NoRouteError:
            output_fn("\nNo alternate route available.")
            logger.warning("No alternate route with closed=%s", sorted(closed))
        else:
            journeys.append(alternate)
            output_fn(format_journey("ALTERNATE ROUTE", alternate))
            output_fn(format_comparison(journey, alternate))

    output_fn("\nThank you for using Metro Route Planner!!")
    logger.info("Session finished")
    return journeys
