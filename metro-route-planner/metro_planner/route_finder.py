"""Route finding algorithms.

* Dijkstra's algorithm  -> route with the smallest total distance (km).
* Breadth-first search  -> route with the fewest stations.

Both accept a set of closed stations which are treated as removed from the
graph, which is how alternate routes are produced.

Complexity: Dijkstra is O((V + E) log V) with a binary heap. The original
version enumerated every possible path (exponential time); this version
scales to large real-world networks.
"""

import heapq
import logging
from collections import deque

from .config import CRITERION_DISTANCE, CRITERION_STOPS
from .exceptions import ClosedStationError, InvalidStationError, NoRouteError

logger = logging.getLogger(__name__)


def _validate_request(metro, start, destination, closed):
    """Raise the appropriate error for bad input before searching."""
    for label, station in (("Start", start), ("Destination", destination)):
        if station not in metro:
            raise InvalidStationError(f"{label} station '{station}' does not exist.")
    for station in closed:
        if station not in metro:
            raise InvalidStationError(f"Closed station '{station}' does not exist.")
    if start in closed:
        raise ClosedStationError(f"Start station '{start}' is closed.")
    if destination in closed:
        raise ClosedStationError(f"Destination station '{destination}' is closed.")


def _build_path(previous, start, destination):
    """Walk the predecessor map backwards to rebuild the route."""
    path = [destination]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return path


def dijkstra_route(metro, start, destination, closed_stations=None):
    """Return the minimum-distance route as a list of stations.

    Ties in distance are broken in favour of fewer stations.
    Raises NoRouteError if the destination is unreachable.
    """
    closed = frozenset(closed_stations or ())
    _validate_request(metro, start, destination, closed)

    best = {start: (0, 0)}            # station -> (distance, stops)
    previous = {}
    visited = set()
    heap = [(0, 0, start)]

    while heap:
        dist, stops, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        if current == destination:
            break
        for neighbour, weight in metro[current].items():
            if neighbour in closed or neighbour in visited:
                continue
            candidate = (dist + weight, stops + 1)
            if neighbour not in best or candidate < best[neighbour]:
                best[neighbour] = candidate
                previous[neighbour] = current
                heapq.heappush(heap, (candidate[0], candidate[1], neighbour))

    if destination not in visited:
        raise NoRouteError(f"No route from {start} to {destination}.")
    return _build_path(previous, start, destination)


def bfs_route(metro, start, destination, closed_stations=None):
    """Return the route with the fewest stations (ignores distances)."""
    closed = frozenset(closed_stations or ())
    _validate_request(metro, start, destination, closed)

    previous = {}
    seen = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if current == destination:
            return _build_path(previous, start, destination)
        for neighbour in metro[current]:
            if neighbour not in seen and neighbour not in closed:
                seen.add(neighbour)
                previous[neighbour] = current
                queue.append(neighbour)
    raise NoRouteError(f"No route from {start} to {destination}.")


def find_route(metro, start, destination, closed_stations=None,
               criterion=CRITERION_DISTANCE):
    """Find a route using the chosen criterion ('distance' or 'stops')."""
    logger.info("Finding route %s -> %s (criterion=%s, closed=%s)",
                start, destination, criterion, sorted(closed_stations or ()))
    if criterion == CRITERION_DISTANCE:
        route = dijkstra_route(metro, start, destination, closed_stations)
    elif criterion == CRITERION_STOPS:
        route = bfs_route(metro, start, destination, closed_stations)
    else:
        raise ValueError(f"Unknown criterion: {criterion!r}")
    logger.info("Route found: %s", " -> ".join(route))
    return route
