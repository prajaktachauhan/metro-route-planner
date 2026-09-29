"""Data model for a planned journey."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Journey:
    """Immutable summary of one route and its computed metrics."""

    route: Tuple[str, ...]
    distance: float          # km
    time_minutes: float
    fare: int

    @property
    def stops(self):
        """Number of hops between stations (route length - 1)."""
        return len(self.route) - 1
