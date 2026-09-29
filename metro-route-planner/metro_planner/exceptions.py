"""Custom exceptions so callers can handle each failure case precisely."""


class MetroError(Exception):
    """Base class for all Metro Route Planner errors."""


class InvalidStationError(MetroError):
    """Raised when a station name does not exist in the network."""


class NoRouteError(MetroError):
    """Raised when no path exists between two stations."""


class ClosedStationError(MetroError):
    """Raised when the start/destination itself is marked as closed."""
