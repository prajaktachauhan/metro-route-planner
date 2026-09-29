"""Helpers for validating and querying the metro graph."""

from collections import deque


def validate_network(metro):
    """Check the graph is well-formed; raise ValueError listing every problem.

    Rules: neighbours must exist, distances must be positive numbers and
    every connection must be stored in both directions with equal distance.
    """
    errors = []
    for station, neighbours in metro.items():
        for other, dist in neighbours.items():
            if other not in metro:
                errors.append(f"{station} -> {other}: unknown station")
                continue
            if not isinstance(dist, (int, float)) or dist <= 0:
                errors.append(f"{station} -> {other}: invalid distance {dist!r}")
            elif metro[other].get(station) != dist:
                errors.append(f"{station} <-> {other}: connection is not symmetric")
    if errors:
        raise ValueError("Invalid metro network:\n  " + "\n  ".join(errors))
    return True


def get_stations(metro):
    """Return station names in alphabetical order."""
    return sorted(metro)


def normalize_station(name, metro):
    """Match user text to a real station name.

    Ignores case and extra spaces, e.g. '  rajiv   CHOWK ' -> 'Rajiv Chowk'.
    Returns None if there is no match.
    """
    key = " ".join(str(name).split()).lower()
    for station in metro:
        if station.lower() == key:
            return station
    return None


def is_connected(metro):
    """True if every station can be reached from every other station."""
    if not metro:
        return True
    start = next(iter(metro))
    seen = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for nxt in metro[current]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen) == len(metro)
