"""Central configuration for the Metro Route Planner.

Keeping constants here (instead of hard-coding them inside functions)
makes the system easy to maintain and tweak.
"""

from pathlib import Path

# ---- Travel model -------------------------------------------------------
AVERAGE_SPEED_KMPH = 30          # average train speed used for time estimate

# ---- Fare model: (max distance in km, fare) ----------------------------
FARE_SLABS = [
    (2, 10),
    (5, 20),
    (10, 30),
    (15, 40),
]
MAX_FARE = 50                    # fare for anything beyond the last slab
CURRENCY = "Rs."                 # plain ASCII so every terminal can print it

# ---- Route selection criteria ------------------------------------------
CRITERION_DISTANCE = "distance"  # minimise total km (Dijkstra)
CRITERION_STOPS = "stops"        # minimise number of stations (BFS)

# ---- Logging ------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "metro_planner.log"
LOG_LEVEL = "INFO"
