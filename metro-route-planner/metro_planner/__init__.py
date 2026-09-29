"""Efficient Metro Route Planner package.

Modules
-------
config          Central constants (speed, fare slabs, logging).
metro_data      The metro network stored as a weighted graph.
graph           Network validation and station-name helpers.
exceptions      Custom exception types.
models          Journey data class.
route_finder    Dijkstra / BFS routing with closed-station support.
calculator      Distance, time and fare calculations.
input_handler   Validated user input.
display         Output formatting.
logger_setup    Logging configuration.
planner         Orchestrates the whole CLI workflow.
"""

__version__ = "2.0.0"
