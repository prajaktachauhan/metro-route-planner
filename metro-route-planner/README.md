# Efficient Metro Route Planner

A command-line application that finds the best route between two metro stations,
estimates the distance, travel time and fare, and recomputes an alternate route
when one or more stations are closed. Built in Python using graph algorithms
(Dijkstra's shortest path and breadth-first search).

## Overview
The metro network is stored as a weighted graph. The user picks a start and a
destination station and a route type (shortest distance or fewest stations). The
planner returns the route with journey details. If a station is closed, the
planner removes it from the graph and computes an alternate route, then shows
how much extra distance, time and money the detour costs.

## Features
- Shortest-distance routing with **Dijkstra's algorithm** (O((V+E) log V)).
- Fewest-stations routing with **BFS**.
- Distance, time and fare calculation (configurable speed and fare slabs).
- **Closed-station handling** for one or several stations, plus original vs. alternate comparison.
- **Input validation**: case-insensitive names, re-prompting, protection against same start/destination, invalid menu choices, etc.
- **Logging** to `logs/metro_planner.log`.
- **Custom exceptions** and a last-resort error guard (no raw tracebacks).
- Network integrity check at startup (missing neighbours, one-way edges, bad distances).
- **50 unit and end-to-end tests**.

## Technologies / tools used
- Python 3.8+ (standard library only: `heapq`, `collections`, `logging`, `dataclasses`, `unittest`)
- Git & GitHub for version control
- Graphviz / ReportLab / Matplotlib (only used to produce the diagrams and PDF report in `docs/`)

## Project structure
```
metro-route-planner/
├── main.py                    # entry point
├── metro_planner/             # application package
│   ├── config.py              # speed, fare slabs, logging settings
│   ├── metro_data.py          # the metro graph
│   ├── graph.py               # validation and station-name helpers
│   ├── exceptions.py          # custom exceptions
│   ├── models.py              # Journey data class
│   ├── route_finder.py        # Dijkstra + BFS with closed stations
│   ├── calculator.py          # distance / time / fare
│   ├── input_handler.py       # validated input
│   ├── display.py             # output formatting
│   ├── logger_setup.py        # logging configuration
│   └── planner.py             # workflow orchestration
├── tests/                     # unit and end-to-end tests
├── docs/                      # project report, diagrams, screenshots
├── logs/                      # runtime logs (git-ignored)
├── statement.md
└── README.md
```

## How to install and run
1. Install Python 3.8 or newer (https://www.python.org/downloads/).
2. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd metro-route-planner
   ```
3. No packages need to be installed (see `requirements.txt`).
4. Run the program:
   ```bash
   python main.py
   ```
5. Follow the prompts: enter the starting station, destination, route type, and
   whether any station is closed. Station names are not case-sensitive.

### Sample session
```
Enter starting station: rajiv chowk
Enter destination station: delhi gate
Enter 1 or 2: 1

RECOMMENDED ROUTE
Rajiv Chowk -> Central Secretariat -> Delhi Gate
Distance: 5 km | Estimated Time: 10.0 minutes | Estimated Cost: Rs. 20

Is any station closed? (yes/no): yes
Enter closed station(s), comma-separated: Central Secretariat

ALTERNATE ROUTE
Rajiv Chowk -> Kashmere Gate -> Chandni Chowk -> Red Fort -> Jama Masjid -> Delhi Gate
Distance: 9 km | Estimated Time: 18.0 minutes | Estimated Cost: Rs. 30
```
More screenshots are in `docs/screenshots/`.

## Instructions for testing
Run the whole suite from the project root:
```bash
python -m unittest discover -s tests -v
```
Expected result: `Ran 50 tests ... OK`. (`pytest` also works if you have it installed.)

| Test file | What it checks |
|---|---|
| `test_graph.py` | network validation, connectivity, name normalisation |
| `test_route_finder.py` | Dijkstra, BFS, closed stations, error cases |
| `test_calculator.py` | distance, time, fare slab boundaries |
| `test_input_handler.py` | every input prompt including invalid entries |
| `test_planner.py` | full user workflow with scripted keyboard input |

## Customising
- Change speed or fares in `metro_planner/config.py`.
- Add stations in `metro_planner/metro_data.py` (add each connection in **both** directions; the program validates this at startup).

## Documentation
The full project report (PDF) with architecture, UML diagrams, design decisions
and testing approach is in `docs/Project_Report.pdf`. Diagram images are in
`docs/diagrams/`.
